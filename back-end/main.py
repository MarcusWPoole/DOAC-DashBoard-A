from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import random
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your dev URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# ——— Load real episodes data ———
df = pd.read_json("episodes_cleaned.json", convert_dates=["release_date"])

@app.get("/api/episodes")
def read_episodes():
    out = []
    for _, r in df.iterrows():
        out.append({
            "episode":         int(r["episode_id"]),
            "title":           r["episode_name"],
            "guest":           r.get("extracted_guest") or None,
            "date":            r["release_date"].strftime("%Y-%m-%d"),
            "views":           int(r["views"]),
            "shares":          int(r["shares"]),
            "avgViewDuration": float(r.get("averageViewPercentage", 0)),
            "subsGained":      int(r.get("subscribersGained", 0)),
            "subsLost":        int(r.get("subscribersLost", 0))
        })
    return out


# @app.get("/api/guest-recommendations")

