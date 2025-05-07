from fastapi import FastAPI, Query, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any, Dict, List
import pandas as pd
import re
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def combine_episode_text(df: pd.DataFrame) -> pd.Series:
    title = df['episode_name'].fillna('')
    desc  = df['episode_description'].fillna('')
    return title + ' ' + desc

    # Load predictive pipeline (ensure the pickle matches this module's scope)
    model = joblib.load('./video_performance_model.pkl')

def prepare_forecast_df(payload: Dict[str, Any], min_date: pd.Timestamp) -> pd.DataFrame:
    """
    Build a DataFrame with model features from input payload.
    """
    # Parse release_date
    date = pd.to_datetime(payload['release_date'])
    df_in = pd.DataFrame([{**payload}])
    df_in['year'] = date.year
    df_in['month'] = date.month
    df_in['day_of_week'] = date.weekday()
    df_in['days_since_first'] = (date - min_date).days
    return df_in


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load cleaned data
df = pd.read_json("episodes_cleaned.json", convert_dates=["release_date"])

# Precomputes smallest date for days_since_first
_min_date = df['release_date'].min()


if 'clean_text_for_topic' not in df.columns:
    df['text_for_topic_raw'] = (
        df['episode_name'].fillna('') + ' ' + df['episode_description'].fillna('')
    )

    def clean_text(text: str) -> str:
        lines = text.split('\n')
        filtered = []
        for line in lines:
            if re.match(r'^\s*\d{1,2}:\d{2}', line):
                continue
            low = line.strip().lower()
            if (low.startswith('topics:') or low.startswith('sponsors:') or
                low.startswith('follow') or low.startswith('this episode') or
                low.startswith('join this channel') or low.startswith('my new book')):
                continue
            filtered.append(line)
        cleaned = ' '.join(filtered)
        cleaned = re.sub(r'http\S+|www\.\S+', ' ', cleaned)
        cleaned = re.sub(r'\d+', ' ', cleaned)
        cleaned = re.sub(r'[^A-Za-z\s]', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned.lower()

    df['clean_text_for_topic'] = df['text_for_topic_raw'].apply(clean_text)

# Run LDA at startup
vectorizer = CountVectorizer(
    max_df=0.85, min_df=3,
    stop_words='english', max_features=1500,
    ngram_range=(1,2)
)
dtm = vectorizer.fit_transform(df['clean_text_for_topic'])
lda = LatentDirichletAllocation(
    n_components=8, max_iter=15,
    learning_method='online', random_state=42
)
W = lda.fit_transform(dtm)
df['lda_topic_id']   = W.argmax(axis=1)
df['lda_topic_prob'] = W.max(axis=1)

# Map client-side metric names to DataFrame columns
METRIC_MAP: Dict[str, str] = {
    "views":            "views",
    "shares":           "shares",
    "likes":            "likes",
    "dislikes":         "dislikes",
    "avgViewDuration":  "averageViewPercentage",
    "subsGained":       "subscribersGained",
    "subsLost":         "subscribersLost"
}

# Helper to convert date strings
def to_date(s: str) -> pd.Timestamp:
    return pd.to_datetime(s)


@app.get("/api/episodes", response_model=Any)
def read_episodes(
    date_from:  Optional[str]   = Query(None, description="YYYY-MM-DD"),
    date_to:    Optional[str]   = Query(None, description="YYYY-MM-DD"),
    metric:     str             = Query("views", description="Which metric to filter on"),
    min_metric: Optional[float] = Query(None, description="Minimum metric value"),
    max_metric: Optional[float] = Query(None, description="Maximum metric value"),
    guest:      Optional[str]   = Query(None, description="Filter by guest name")
):
    if metric not in METRIC_MAP:
        raise HTTPException(status_code=400, detail=f"Unknown metric '{metric}'")
    col = METRIC_MAP[metric]

    data = df.copy()
    if date_from:
        data = data[data.release_date >= to_date(date_from)]
    if date_to:
        data = data[data.release_date <= to_date(date_to)]
    if guest:
        data = data[data.extracted_guest == guest]

    vals = pd.to_numeric(data[col], errors="coerce").dropna()
    metric_min = float(vals.min()) if not vals.empty else 0.0
    metric_max = float(vals.max()) if not vals.empty else 0.0

    if min_metric is not None:
        data = data[pd.to_numeric(data[col], errors="coerce").fillna(0) >= min_metric]
    if max_metric is not None:
        data = data[pd.to_numeric(data[col], errors="coerce").fillna(0) <= max_metric]

    episodes_out = []
    for _, r in data.iterrows():
        episodes_out.append({
            "episode":         int(r["episode_num"]),
            "title":           r["episode_name"],
            "guest":           r.get("guest") or None,
            "date":            r["release_date"].strftime("%Y-%m-%d"),
            "views":           int(r["views"]),
            "shares":          int(r["shares"]),
            "likes":           int(r.get("likes", 0)),
            "dislikes":        int(r.get("dislikes", 0)),
            "avgViewTime":     int(r.get("averageViewDuration")),
            "avgViewDuration": float(r.get("averageViewPercentage", 0)),
            "subsGained":      int(r.get("subscribersGained", 0)),
            "subsLost":        int(r.get("subscribersLost", 0)),
            "thumbnail":       r.get("thumbnail_url")
        })

    return {
        "episodes":  episodes_out,
        "metricMin": metric_min,
        "metricMax": metric_max
    }

@app.get("/api/episodes/bounds", response_model=Any)
def read_metric_bounds(
    date_from:  Optional[str]   = Query(None, description="YYYY-MM-DD"),
    date_to:    Optional[str]   = Query(None, description="YYYY-MM-DD"),
    metric:     str             = Query("views", description="Which metric to get bounds for"),
    guest:      Optional[str]   = Query(None, description="Filter by guest name")
):
    if metric not in METRIC_MAP:
        raise HTTPException(status_code=400, detail=f"Unknown metric '{metric}'")
    col = METRIC_MAP[metric]

    data = df.copy()
    if date_from:
        data = data[data.release_date >= to_date(date_from)]
    if date_to:
        data = data[data.release_date <= to_date(date_to)]
    if guest:
        data = data[data.extracted_guest == guest]

    vals = pd.to_numeric(data[col], errors="coerce").dropna()
    metric_min = float(vals.min()) if not vals.empty else 0.0
    metric_max = float(vals.max()) if not vals.empty else 0.0

    return {
        "metricMin": metric_min,
        "metricMax": metric_max
    }

@app.get("/api/metrics", response_model=List[Dict[str, str]])
def list_metrics():
    """
    Return available metrics with human-readable labels.
    """
    metrics: List[Dict[str, str]] = []
    for key in METRIC_MAP.keys():
        label = re.sub(r"(?<!^)(?=[A-Z])", " ", key).capitalize()
        metrics.append({"value": key, "label": label})
    return metrics


@app.get("/api/episodes/summary", response_model=dict)
def summary() -> dict:
    data = df.copy()

    total_episodes  = int(len(data))
    total_views     = int(data["views"].sum())
    # seconds → minutes to one decimal
    avg_view_min    = round(data["averageViewDuration"].dropna().mean() / 60, 1)

    # Most-watched episode
    top_ep_row      = data.loc[data["views"].idxmax()]
    top_episode     = {
        "episode": int(top_ep_row["episode_num"]),
        "title"  : str(top_ep_row["episode_name"]),
        "views"  : int(top_ep_row["views"])
    }

    # Guest whose episodes have the highest cumulative views
    guest_views     = (
        data.dropna(subset=["guest"])
            .groupby("guest")["views"]
            .sum()
    )
    if guest_views.empty:
        top_guest = {"name": None}
    else:
        guest_name  = guest_views.idxmax()
        top_guest   = {"name": guest_name, "views": int(guest_views.max())}

    return {
        "totalEpisodes": total_episodes,
        "totalViews"   : total_views,
        "avgViewMin"   : avg_view_min,
        "topEpisode"   : top_episode,
        "topGuest"     : top_guest,
    }
    

@app.get("/api/episodes/guest-recurring", response_model=List[dict])
def recurring_guest_appearance_subs_to_views(
    date_from: Optional[str] = Query(None, description="YYYY-MM-DD")
):
    # Step 1: identify recurring guests in full dataset
    all_guests = df[df["guest"].notna()]
    recurring_guests = all_guests["guest"].value_counts()
    recurring_guests = recurring_guests[recurring_guests > 1].index

    # Step 2: filter episodes to selected range
    data = df.copy()
    if date_from:
        data = data[data["release_date"] >= to_date(date_from)]
    data = data[data["guest"].isin(recurring_guests)]

    # Step 3: compute ratio
    data["subs_to_views_ratio"] = (
        pd.to_numeric(data["subscribersGained"], errors="coerce") /
        pd.to_numeric(data["views"], errors="coerce")
    )

    # Step 4: assign appearance numbers
    data["appearance_num"] = (
        data.groupby("guest")["episode_num"]
        .rank(method="first")
        .astype(int)
    )

    result = data[["guest", "appearance_num", "subs_to_views_ratio"]]
    return result.dropna(subset=["subs_to_views_ratio"]).to_dict(orient="records")


@app.get("/api/episodes/correlation", response_model=List[dict])
def correlation_kpis_to_subs(
    date_from: Optional[str] = Query(None, description="YYYY-MM-DD")
):
    df_clean = df[[col for col in df.columns if 'log' not in col and 'scaled' not in col]].copy()

    if date_from:
        df_clean = df_clean[df_clean["release_date"] >= to_date(date_from)]

    targets = ['subscribersGained', 'subscribersLost']
    kpis = df_clean.select_dtypes(include='number').drop(columns=targets, errors='ignore').columns

    records = []
    for target in targets:
        for kpi in kpis:
            r, p = pearsonr(df_clean[target], df_clean[kpi])
            records.append({
                'target': target,
                'kpi': kpi,
                'pearson_r': r,
                'p_value': p
            })
    return records

@app.get("/api/episodes/content-efficiency", response_model=List[dict])
def content_efficiency_quadrants(
    date_from: Optional[str] = Query(None, description="YYYY-MM-DD")
):
    data = df.copy()
    if date_from:
        data = data[data["release_date"] >= to_date(date_from)]

    data = data[["episode_num", "episode_name", "views", "averageViewDuration"]].dropna()

    views_median = data["views"].median()
    duration_median = data["averageViewDuration"].median()

    def bucket(row):
        if row["views"] < views_median and row["averageViewDuration"] > duration_median:
            return "High Attention, Low Exposure"
        elif row["views"] >= views_median and row["averageViewDuration"] > duration_median:
            return "High Attention, High Exposure"
        elif row["views"] < views_median and row["averageViewDuration"] <= duration_median:
            return "Low Attention, Low Exposure"
        else:
            return "Low Attention, High Exposure"

    data["content_efficiency"] = data.apply(bucket, axis=1)
    return data.rename(columns={
        "episode_num": "episode",
        "episode_name": "title"
    }).to_dict(orient="records")
    

@app.get("/api/topics/performance", response_model=List[Dict[str, Any]])
def topic_performance(date_from: Optional[str] = Query(None, description="YYYY-MM-DD")):
    topic_labels = {
        0: "Health & Wellness",
        1: "Business and Entrepreneurship",
        2: "Technology",
        3: "Social Issues",
        4: "Leadership",
        5: "Personal Growth",
        6: "Relationships",
        7: "Life Style"
    }
    data = df.copy()
    if date_from:
        data = data[data["release_date"] >= to_date(date_from)]

    # Map IDs to labels
    data['topic'] = data['lda_topic_id'].map(topic_labels)
    grouped = (
        data.groupby('topic')
            .agg(
                avg_views=('views', 'mean'),
                avg_engagement=('averageViewPercentage', 'mean'),
                episode_count=('topic', 'count')
            )
            .reset_index()
    )
    return grouped.to_dict(orient='records')

# --- Forecast endpoint ---
class ForecastRequest(BaseModel):
    episode_name: str
    episode_description: str
    guest: str
    release_date: str  # YYYY-MM-DD

class ForecastResponse(BaseModel):
    views: float
    estimatedMinutesWatched: float
    subscribersGained: float
    likes: float
    dislikes: float
    averageViewPercentage: float

@app.post("/api/forecast", response_model=ForecastResponse)
def forecast(request: ForecastRequest):
    """
    Predict KPIs for a new episode.
    """
    # Prepare input DataFrame
    payload = request.dict()
    df_feat = prepare_forecast_df(payload, _min_date)

    # Ensure text combination matches pipeline
    df_feat['episode_name'] = df_feat['episode_name']
    df_feat['episode_description'] = df_feat['episode_description']
    df_feat['guest'] = df_feat['guest']

    preds = model.predict(df_feat)
    # Map target order to keys
    keys = ['views', 'estimatedMinutesWatched', 'subscribersGained', 'likes', 'dislikes', 'averageViewPercentage']
    values = preds.flatten().tolist()
    return ForecastResponse(**dict(zip(keys, values)))