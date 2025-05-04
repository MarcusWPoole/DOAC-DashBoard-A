# backend/main.py

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Any, Optional
import pandas as pd

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

# Map client‐side metric names to DataFrame columns
METRIC_MAP = {
    "views":            "views",
    "shares":           "shares",
    "likes":            "likes",
    "dislikes":         "dislikes",
    "avgViewDuration":  "averageViewPercentage",
    "subsGained":       "subscribersGained",
    "subsLost":         "subscribersLost"
}

def to_date(s: str) -> pd.Timestamp:
    return pd.to_datetime(s)

@app.get("/api/episodes", response_model=Any)
def read_episodes(
    date_from:  Optional[str]  = Query(None, description="YYYY-MM-DD"),
    date_to:    Optional[str]  = Query(None, description="YYYY-MM-DD"),
    metric:     str            = Query("views", description="Which metric to filter on"),
    min_metric: Optional[float]= Query(None, description="Minimum metric value"),
    max_metric: Optional[float]= Query(None, description="Maximum metric value"),
    guest:      Optional[str]  = Query(None, description="Filter by guest name")
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
        data = data[data[col] >= min_metric]
    if max_metric is not None:
        data = data[data[col] <= max_metric]


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
            "avgViewDuration": float(r.get("averageViewPercentage", 0)),
            "subsGained":      int(r.get("subscribersGained", 0)),
            "subsLost":        int(r.get("subscribersLost", 0))
        })

    return {
        "episodes":  episodes_out,
        "metricMin": metric_min,
        "metricMax": metric_max
    }
