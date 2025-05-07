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




# Future Extensions:

I believe the extension that would have the greatest impact on the results a product like this could deliver is a working guest recommendation system. The main blocker I faced here was the lack of an official API for Google Trends. The unofficial alternatives available are unreliable, they tend to get flagged as bots and either rate-limited or blacklisted, making them unsuitable for production use. That said, I recall Isaac mentioning that it’s often better to get something currently not possible 80% of the way there rather than hold back entirely, so I went ahead and built the tool using dummy data to validate the concept. With a reliable trends signal in place, this feature could increase audience engagement by surfacing timely and in-demand guest suggestions. Or strealine the search process when a topic of interest is identified. To further this I would use google's custom search engine api to perform searches based on key words or topics extracted from the tool and filter it to discover guests either through web scraping or feeding the the result through an LLM. The results of this process could then be explored by the guest booking team speeding up initial discovery time.

Another extension would be integrating a large language model to automatically generate the key findings on the InsightsfulTrends page. This model would ingest data directly from the displayed graphs or a structured analysis layer, and translate it into clear, concise, copy-ready insights for dashboard users. These summaries would be phrased in a way that’s professional and easy to understand, suitable for executive reporting or stakeholder sharing. Additionally, insights could update in real time whenever new, significant trends are detected, delivering useable insights the moment a user lands on the page. This process would accelerate decision-making by highlighting impactful opportunities without the need for manual interpretation, removing the need for a technical middleman.
