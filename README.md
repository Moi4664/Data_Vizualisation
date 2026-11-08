# NYC Taxi Explorer: Streamlit Dashboard + CV

**Student:** KARAKOZIAN · **Student ID:** 20231654 · **Class:** BDML2 · **Year:** 2026

An interactive, bilingual (French/English) NYC taxi trip analysis using Streamlit, Pandas and Plotly, plus a CV page. This submission is named for the **20-mark Streamlit option**. Confirm any additional course content required by your instructor.

## Features

- Bilingual interface (French/English): click the 🇫🇷/🇬🇧 flag buttons in the sidebar to switch — every page, chart, filter and label is translated
- Dashboard with date, hour, weekday and trip distance filters
- KPI cards (trip count, distance, duration, implied speed)
- Hourly and weekday demand charts
- Distribution of trip distances and duration–distance scatter plot
- Interactive pickup map (Carto Positron)
- Raw missingness and data-cleaning summary
- Data-aware business insights and CSV / HTML figure downloads
- CV page with the current CV content in both languages, plus a PDF download of the matching LaTeX-built CV (`CV/CV_KARAKOZIAN_Varoujan_FR.pdf` / `_EN.pdf`)

## Project structure

```text
TP_CV_D2_20231654_BDML2/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Launch the Streamlit dashboard

```bash
python -m streamlit run app.py
```

Open the local address printed in the terminal (usually `http://localhost:8501`). The app requires an internet connection when downloading the CSV and rendering basemap tiles.

When finished, deactivate with `deactivate`.

## Data source

[Kepler.gl NYC taxi trip sample](https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv).

The original CSV is downloaded when you start the application; the dataset is **not committed** to this repository. The first download may take a little longer; Streamlit caches the result for one day.

## Data quality and limitations

- Parse pickup and drop-off timestamps; derive `duration_min`, `hour`, `weekday`, and `date`.
- Keep trips with distance 0.01–100 miles, duration 0.5–240 minutes, pickup within a broad NYC bounding box, and estimated speed 0.1–80 mph.
- The time zone represented in the original timestamp string has not been independently verified.
- Insights are descriptive for this sample, **not** representative NYC-wide taxi traffic estimates.
- Estimated speed is based on reported trip distance and duration and cannot prove congestion.

## GitHub submission

Commit `app.py`, `requirements.txt`, `README.md`, `.gitignore`, and the `CV/` folder (LaTeX sources, photo, and compiled PDFs). If your professor requires an online application, deploy the repository through [Streamlit Community Cloud](https://share.streamlit.io/) and submit both the GitHub URL and the app URL.

## AI assistance disclosure

This project (notebook, Streamlit app, and supporting write-ups) was built with the help of an AI assistant (Claude, Anthropic), used for code structure, chart design, and parts of the written analysis. Disclosed here for transparency.
