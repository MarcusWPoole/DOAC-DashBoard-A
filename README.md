# Diary of a CEO Analytics Dashboard

A responsive Svelte front‑end with a FastAPI back‑end for exploring and analysing “Diary of a CEO” podcast episode performance.

---

## Getting Started

### Prerequisites

- **Node.js** v16+ & **npm**  
- **Python** 3.9+ & **pip**

### Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/MarcusWPoole/DOAC-DashBoard-A.git
   cd DOAC-DashBoard-A

2. **Package Installation**  
   ```terminal
   ./run-all.sh

   Access at: http://127.0.0.1:5173/



### Tech Stack
#### Front‑end:
Svelte - reactive components

Vite - development server & bundler

Tailwind CSS - utility‑first styling

Chart.js via svelte-chartjs - interactive charts

D3 - data‑driven DOM manipulations

Plotly.js - advanced interactive visualisations

date‑fns - date formatting

svelte-range-slider-pips - range slider with pips

svelte-routing - client‑side routing

#### Back‑end:
FastAPI - high‑performance REST API

Uvicorn - ASGI server

Pandas - CSV loading and data manipulation

python‑dateutil - robust date parsing

NumPy - numerical operations

SciPy - statistical utilities

scikit‑learn & joblib - simple predictive prototype


#### Data Analysis:
pandas, NumPy, SciPy - data loading, cleaning, numerical & statistical routines

scikit‑learn - pipelines, transformers, regressors (GradientBoostingRegressor, TimeSeriesSplit)

category_encoders - target and binary encoding for categorical features

TfidfVectorizer - text‑based features on episode_description

pytrends - Google Trends API to pull search‑volume time series for guest names or keywords

matplotlib - exploratory plots, custom tick formatting

joblib - serialising trained models & transformers


## Data Wrangling:

### Episode ID:

Uses episode_num as a numeric, unique identifier (original episode_id contained non‑numeric strings).

### Guest Extraction:
Employed a SpaCy Named Entity Recognition model to parse out guest names from episode_description.

The NER approach correctly identified around 80% of guests.

For the remaining 20%, manual corrections were applied directly in the dataset to ensure accuracy.

Where still unknown e.g. solo episode, guest name was left as "unknown"

### Limited data for training

Only ~300 episodes: opted for tree‑based models (LightGBM/XGBoost or GradientBoosting) with strong regularisation rather than deep networks.

### Feature engineering

Temporal: extracted year, month, day‑of‑week, days‑since‑first against the earliest episode.

Text: concatenated title + description → TF‑IDF (max 200 features).


### Text cleaning for LDA

Stripped out timestamps (e.g. “00:15”), sponsor/promotional boilerplate, URLs, digits, non‑alphabetic characters, and collapsed whitespace.

LDA with 8 topics to label each episode for thematic analysis, probably not accurate to number of podcast topics.

