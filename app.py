"""NYC Taxi Explorer: bilingual (FR/EN) Streamlit project for BDML2.

Run locally: streamlit run app.py
"""
from __future__ import annotations

from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

DATA_URL = "https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv"
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
ROOT = Path(__file__).resolve().parent
CV_DIR = ROOT / "CV"

WEEKDAY_LABELS = {
    "en": {d: d for d in WEEKDAYS},
    "fr": {
        "Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
        "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi", "Sunday": "Dimanche",
    },
}

CHECK_KEYS = ["valid_time", "distance_range", "duration_range", "location_box", "speed_range", "all_passed"]

CV_CONTENT = {
    "fr": {
        "role": "Apprenti Ingénieur IA chez Dassault Systèmes",
        "contact": "+33 7 81 78 53 77  ·  Varoujan.Karakozian@efrei.net  ·  3 rue des Œillets, 94140 Alfortville  ·  03/11/2005",
        "profile_header": "Profil",
        "profile": "Apprenti ingénieur en 2ᵉ année de cycle ingénieur à l'EFREI Paris, spécialisation **Big Data & Machine Learning (BDML)**. En alternance de trois ans (2025-2028) chez **Dassault Systèmes**, au sein d'une équipe R&D DevSecOps dédiée à l'assistance IA des développeurs internes, où je développe des outils reposant sur les protocoles **MCP** et **RAG**.",
        "education_header": "Formation",
        "education": [
            ("Cycle Ingénieur, spécialisation Big Data & Machine Learning", "EFREI Paris (en alternance)", "2025 – 2028", "2ᵉ année en cours."),
            ("Classe préparatoire intégrée internationale (anglais)", "EFREI Paris", "", ""),
            ("Baccalauréat, mention Bien", "Lycée Sainte-Marie, Créteil", "", ""),
        ],
        "experience_header": "Expérience",
        "experience": [
            {
                "title": "Apprenti Ingénieur IA",
                "place": "Dassault Systèmes, Vélizy-Villacoublay",
                "dates": "Sept. 2025 – Juin 2028",
                "bullets": [
                    "Développement d'outils **MCP** (Model Context Protocol) connectant un assistant de code IA aux systèmes internes : détection automatique du contexte de versionnement, récupération de métadonnées de build, collecte de données via scraping web automatisé (Selenium).",
                    "Conception et évaluation d'un pipeline **RAG** local pour l'indexation de documentation interne (BM25), en remplacement d'une approche basée LLM 2 à 3 ordres de grandeur plus lente et coûteuse en tokens.",
                    "Mise en place d'un protocole d'évaluation à trois modèles (génération de questions, réponse, LLM-as-judge) mesurant l'Accuracy@K du retrieval sur environ 8 500 questions réparties sur 3 corpus.",
                    "Contribution à **FixGen**, un outil d'IA générative de diagnostic de crashs logiciels : développement des outils de collecte de données (classification d'URL, scraping automatisé de stack traces).",
                ],
            },
            {
                "title": "Stage Commercial",
                "place": "Lacoste, Créteil",
                "dates": "2025 (1 mois)",
                "bullets": [
                    "Accueil et conseil des clients, recommandations personnalisées adaptées à leurs besoins.",
                    "Utilisation de compétences linguistiques (anglais, espagnol) pour conseiller une clientèle étrangère.",
                ],
            },
            {
                "title": "Stage Ouvrier (préparateur de commande)",
                "place": "Phoenix Pharma, Créteil",
                "dates": "2024 (1 mois)",
                "bullets": [
                    "Gestion logistique : préparation et vérification de commandes pharmaceutiques.",
                    "Travail d'équipe : collaboration efficace avec les équipes d'entrepôt dans un environnement dynamique.",
                ],
            },
        ],
        "projects_header": "Projets académiques",
        "projects_recent": [
            ("NYC Taxi: Data Visualization & Business Intelligence", "2026", "Analyse exploratoire de courses de taxi new-yorkaises (Python, Pandas, Plotly, Streamlit) : nettoyage de données, visualisations interactives, dashboard de BI avec KPIs. *(Ce projet.)*"),
            ("Classification de la qualité du vin : Machine Learning", "2026", "Comparaison de plusieurs modèles (Random Forest, SVM, etc.) pour prédire la qualité d'un vin à partir de ses caractéristiques physico-chimiques."),
        ],
        "projects_earlier_label": "Projets antérieurs",
        "projects_earlier": "**Analyse du changement climatique** (2025) : ACP de A à Z, corrélation inégalité/pollution nationale. **Voll'Effrei** (2025) : jeu vidéo de volley-ball, projet interdisciplinaire physique/informatique. **Chatbot intelligent** (2024) : chatbot Python basé sur l'analyse TF-IDF. **CDataFrame** (2024) : DataFrame en langage C inspiré de Pandas.",
        "skills_header": "Compétences",
        "skills": [
            ("IA / Machine Learning", ["MCP (Model Context Protocol)", "RAG & évaluation de RAG", "LLM-as-judge, Accuracy@K", "BM25, scikit-learn (Random Forest, SVM)"]),
            ("Programmation", ["Python, C, Java"]),
            ("Outils & plateformes", ["Git/GitHub, Linux", "Selenium, Streamlit, Plotly, Pandas"]),
            ("Bases de données", ["SQL, MySQL, SQLite"]),
            ("Soft skills", ["Travail en équipe", "Capacité d'adaptation", "Autodidacte", "Sens de l'initiative", "Créatif", "Autonomie", "Polyvalent"]),
        ],
        "languages_header": "Langues",
        "languages": ["Français : langue maternelle", "Anglais : avancé B2", "Arménien : intermédiaire B1", "Espagnol : intermédiaire B1"],
        "hobbies_header": "Loisirs",
        "hobbies": ["Musique", "Escalade", "Échecs", "Basketball"],
        "download_label": "📄 Télécharger le CV (PDF)",
        "pdf_file": "CV_KARAKOZIAN_Varoujan_FR.pdf",
    },
    "en": {
        "role": "AI Engineer Apprentice at Dassault Systèmes",
        "contact": "+33 7 81 78 53 77  ·  Varoujan.Karakozian@efrei.net  ·  3 rue des Œillets, 94140 Alfortville, France  ·  Born 3 Nov 2005",
        "profile_header": "Profile",
        "profile": "Second-year engineering student at EFREI Paris, specializing in **Big Data & Machine Learning (BDML)**. Currently on a three-year work-study program (2025-2028) with **Dassault Systèmes**, in an R&D DevSecOps team building AI tooling for internal developers, working with **MCP** and **RAG**.",
        "education_header": "Education",
        "education": [
            ("Engineering Cycle, Big Data & Machine Learning specialization", "EFREI Paris (work-study)", "2025 – 2028", "2nd year in progress."),
            ("International Preparatory Classes (English track)", "EFREI Paris", "", ""),
            ("Baccalauréat (French high-school diploma), High Honors", "Lycée Sainte-Marie, Créteil", "", ""),
        ],
        "experience_header": "Experience",
        "experience": [
            {
                "title": "AI Engineer Apprentice",
                "place": "Dassault Systèmes, Vélizy-Villacoublay, France",
                "dates": "Sept. 2025 – Jun 2028",
                "bullets": [
                    "Built **MCP** (Model Context Protocol) tools connecting an AI coding assistant to internal systems: automatic version-control context detection, build metadata retrieval, automated web-scraping data collection (Selenium).",
                    "Designed and evaluated a local **RAG** pipeline (BM25) for internal documentation indexing, replacing an LLM-based approach that was 2–3 orders of magnitude slower and more token-expensive.",
                    "Built a three-model evaluation protocol (question generation, answering, LLM-as-judge) measuring retrieval Accuracy@K across roughly 8,500 questions over 3 benchmark corpora.",
                    "Contributed to **FixGen**, a generative-AI crash diagnosis tool: built data-collection tools (URL classification, automated stack-trace scraping).",
                ],
            },
            {
                "title": "Sales Internship",
                "place": "Lacoste, Créteil, France",
                "dates": "2025 (1 month)",
                "bullets": [
                    "Welcomed and advised customers, providing personalized recommendations tailored to their needs.",
                    "Used language skills (English, Spanish) to assist international customers.",
                ],
            },
            {
                "title": "Warehouse Internship (Order Picker)",
                "place": "Phoenix Pharma, Créteil, France",
                "dates": "2024 (1 month)",
                "bullets": [
                    "Logistics: preparing and checking pharmaceutical orders.",
                    "Teamwork: effective collaboration with warehouse teams in a fast-paced environment.",
                ],
            },
        ],
        "projects_header": "Academic Projects",
        "projects_recent": [
            ("NYC Taxi: Data Visualization & Business Intelligence", "2026", "Exploratory analysis of NYC taxi trips (Python, Pandas, Plotly, Streamlit): data cleaning, interactive visualizations, BI dashboard with KPIs. *(This project.)*"),
            ("Wine Quality Classification: Machine Learning", "2026", "Compared multiple models (Random Forest, SVM, etc.) to predict wine quality from physicochemical features."),
        ],
        "projects_earlier_label": "Earlier projects",
        "projects_earlier": "**Climate Change Data Analysis** (2025): full PCA pipeline showing a correlation between inequality and national pollution. **Voll'Effrei** (2025): volleyball video game, interdisciplinary physics/CS project. **Intelligent Chatbot** (2024): Python chatbot based on TF-IDF analysis. **CDataFrame** (2024): a C-language DataFrame inspired by Pandas.",
        "skills_header": "Skills",
        "skills": [
            ("AI / Machine Learning", ["MCP (Model Context Protocol)", "RAG & RAG evaluation", "LLM-as-judge, Accuracy@K", "BM25, scikit-learn (Random Forest, SVM)"]),
            ("Programming", ["Python, C, Java"]),
            ("Tools & platforms", ["Git/GitHub, Linux", "Selenium, Streamlit, Plotly, Pandas"]),
            ("Databases", ["SQL, MySQL, SQLite"]),
            ("Soft skills", ["Teamwork", "Adaptability", "Self-taught", "Initiative", "Creative", "Autonomous", "Versatile"]),
        ],
        "languages_header": "Languages",
        "languages": ["French: Native", "English: Advanced (B2)", "Armenian: Intermediate (B1)", "Spanish: Intermediate (B1)"],
        "hobbies_header": "Hobbies",
        "hobbies": ["Music", "Climbing", "Chess", "Basketball"],
        "download_label": "📄 Download CV (PDF)",
        "pdf_file": "CV_KARAKOZIAN_Varoujan_EN.pdf",
    },
}

T = {
    "fr": {
        "app_title": "🚕 NYC Taxi Explorer",
        "sidebar_caption": "BDML2 · 2026 · Étudiant 20231654",
        "source_caption": "Source : échantillon public Kepler.gl de taxis NYC",
        "pages_label": "Pages",
        "nav": {"dashboard": "📊 Tableau de bord", "quality": "🧹 Qualité des données", "cv": "👤 CV", "about": "ℹ️ Projet & méthodologie"},
        "loading_raw": "Téléchargement des courses de taxi NYC…",
        "loading_clean": "Nettoyage des données…",
        "load_error_title": "Impossible de charger ou préparer les données : {exc}",
        "load_error_hint": "Vérifiez votre connexion internet et l'accessibilité de la source.",
        "empty_after_clean": "Tous les enregistrements ont été exclus par les règles de nettoyage. Vérifiez la qualité des données.",
        "graph_download": "Télécharger le graphique interactif (HTML)",
        "dashboard": {
            "title": "📊 Tableau de bord de la demande de taxis NYC",
            "caption": "Analyse interactive des courses de taxi : filtrez l'échantillon, explorez les tendances de mobilité et interprétez les résultats.",
            "filters_header": "Filtres du tableau de bord",
            "f_dates": "Dates de prise en charge",
            "f_hours": "Plage horaire de prise en charge",
            "f_weekdays": "Jours de la semaine",
            "f_distance": "Distance de la course (miles)",
            "f_points": "Points sur la carte",
            "empty_selection": "Aucun enregistrement ne correspond à ces filtres. Élargissez la sélection d'heure, de date, de jour ou de distance.",
            "kpi_selected": "Courses sélectionnées",
            "kpi_avg_distance": "Distance moy.",
            "kpi_median_distance": "Distance médiane",
            "kpi_avg_duration": "Durée moy.",
            "kpi_median_speed": "Vitesse médiane",
            "selection_caption": "{sel:,} courses sur {total:,} valides sélectionnées ; {excluded:,} enregistrements bruts exclus lors du nettoyage.",
            "tabs": ["⏰ Temps & demande", "📏 Distance & durée", "📍 Géographie des prises en charge"],
            "hourly_title": "Prises en charge par heure enregistrée",
            "hourly_x": "Heure de prise en charge", "hourly_y": "Courses",
            "weekday_title": "Prises en charge par jour de la semaine",
            "weekday_x": "Jour de la semaine", "weekday_y": "Courses",
            "tab1_info": "Les comptages reflètent **l'échantillon et les filtres**, pas le total des courses à l'échelle de la ville. Un jour avec plus d'enregistrements peut simplement être mieux représenté dans l'échantillon.",
            "hist_title": "Distribution des distances de course (≤ 99ᵉ percentile)",
            "hist_x": "Distance (miles)",
            "hist_caption": "L'écrêtage s'applique uniquement à l'histogramme affiché, pas aux KPI ni aux filtres.",
            "speed_title": "Vitesse médiane implicite par heure de prise en charge",
            "speed_x": "Heure de prise en charge", "speed_y": "Vitesse médiane (mph)",
            "scatter_title": "Durée de course en fonction de la distance (échantillon)",
            "scatter_x": "Distance (miles)", "scatter_y": "Durée (min)", "scatter_color": "Heure",
            "scatter_caption": "Les courses plus longues durent souvent plus longtemps, mais des différences de durée seules ne prouvent ni congestion ni ses causes.",
            "geo_subheader": "Localisations des prises en charge",
            "geo_title": "Localisations des prises en charge ({n:,} courses échantillonnées)",
            "geo_caption": "Les points affichés sont un échantillon aléatoire reproductible. Les clusters visibles indiquent une concentration observée des prises en charge, pas une demande ajustée à la population.",
            "insights_header": "🧠 Enseignements métier pour les filtres sélectionnés",
            "insight_peak": "**Heure de pointe :** {hour}:00 concentre le plus de prises en charge sélectionnées. Les décisions d'effectifs doivent reposer sur une période plus longue et représentative avant toute application opérationnelle.",
            "insight_short": "**Courses courtes :** {pct:.1f}% des courses sélectionnées font **2 miles ou moins**, ce qui indique à quel point l'échantillon est orienté vers les trajets courts.",
            "insight_corr": "**Distance et durée :** corrélation de Pearson = **{corr}** ; l'interprétation demande de la prudence car l'itinéraire, l'horaire et la météo peuvent aussi influencer la durée.",
            "insight_spatial": "**Usage spatial :** examinez la carte des prises en charge pour les clusters observés ; toute affirmation sur un aéroport ou un arrondissement nécessite une validation géographique séparée.",
            "download_filtered": "Télécharger les enregistrements filtrés (CSV)",
            "footer": "Analyse à but pédagogique uniquement · Pas une vue en temps réel de la demande de taxis NYC.",
            "corr_undefined": "non définie",
        },
        "quality": {
            "title": "🧹 Qualité des données & préparation",
            "m_raw": "Lignes brutes", "m_valid": "Lignes valides", "m_excluded": "Lignes exclues",
            "m_excluded_delta": "{pct:.1%} des données brutes",
            "missing_subheader": "Valeurs manquantes dans les données brutes",
            "missing_chart_title": "Données manquantes par colonne (top 15)",
            "missing_y": "Manquant (%)", "missing_x": "Champ source",
            "validation_subheader": "Règles de validation",
            "validation_caption": "Chaque compte « Lignes passant le contrôle » est indépendant. Ne pas additionner les exclusions : un enregistrement peut échouer à plusieurs règles.",
            "sample_subheader": "Échantillon de lignes nettoyées",
            "download_csv": "Télécharger les données nettoyées (CSV)",
            "checks": {
                "valid_time": "Horodatages et heure de prise en charge valides",
                "distance_range": "Distance (0,01–100 miles)",
                "duration_range": "Durée (0,5–240 minutes)",
                "location_box": "Prise en charge dans le périmètre NYC",
                "speed_range": "Vitesse moyenne (0,1–80 mph)",
                "all_passed": "Tous les contrôles réussis",
            },
            "col_check": "Contrôle", "col_passing": "Lignes passant le contrôle",
        },
        "cv": {"title": "👤 Curriculum Vitae"},
        "about": {
            "title": "ℹ️ Projet & méthodologie",
            "body": """### Objectif
Explorer **quand**, **où** et **sur quelle distance** les courses de taxi new-yorkaises ont lieu, à l'aide de graphiques interactifs et d'indicateurs métier utiles.

### Jeu de données
[Échantillon de courses de taxi Kepler.gl](https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv). Le jeu de données est téléchargé à l'exécution et mis en cache pendant un jour.

### Préparation
- Analyse des horodatages de prise en charge et de dépose ; calcul de la durée, de l'heure, du jour de la semaine et de la date.
- Exclusion des courses avec horodatages manquants/invalides, distances hors de **0,01–100 miles**, durées hors de **0,5–240 minutes**, coordonnées de prise en charge hors d'un large périmètre NYC, et vitesses estimées hors de **0,1–80 mph**.
- Le périmètre géographique est une **approximation**, pas une limite administrative officielle de NYC.

### Avertissements d'interprétation
- Cet échantillon peut ne pas représenter toutes les dates ou tous les taxis de NYC ; les pics observés sont donc **spécifiques à l'échantillon**.
- L'heure de prise en charge est lue telle qu'enregistrée dans la chaîne source ; sa sémantique de fuseau horaire exacte n'est pas vérifiée.
- La distance est exprimée en **miles**. La vitesse implicite est la distance divisée par la durée du trajet, **pas** une mesure directe du trafic.
- Une forte densité de prises en charge ne prouve pas à elle seule où se situe la demande la plus forte à NYC.
- La carte utilise un sous-échantillon reproductible pour garder l'interface réactive.

### Comment reproduire
Installez `requirements.txt`, lancez `streamlit run app.py`, et utilisez les filtres de la barre latérale. La version notebook peut être conservée dans le même dépôt GitHub.

### Déclaration d'assistance par IA
Ce projet (notebook, application Streamlit, et écrits associés) a été réalisé avec l'aide d'un assistant IA (Claude, Anthropic), utilisé pour la structure du code, la conception des graphiques et une partie de l'analyse rédigée. Déclaré ici en toute transparence.
""",
        },
    },
    "en": {
        "app_title": "🚕 NYC Taxi Explorer",
        "sidebar_caption": "BDML2 · 2026 · Student 20231654",
        "source_caption": "Source: public Kepler.gl NYC taxi sample",
        "pages_label": "Pages",
        "nav": {"dashboard": "📊 Dashboard", "quality": "🧹 Data quality", "cv": "👤 CV", "about": "ℹ️ Project & methodology"},
        "loading_raw": "Downloading NYC taxi trips…",
        "loading_clean": "Cleaning taxi records…",
        "load_error_title": "Could not load or prepare the dataset: {exc}",
        "load_error_hint": "Check your internet connection and ensure the source URL is accessible.",
        "empty_after_clean": "All records were excluded by cleaning rules. Review the data quality checks.",
        "graph_download": "Download interactive HTML",
        "dashboard": {
            "title": "📊 NYC Taxi Demand Dashboard",
            "caption": "Interactive analysis of taxi trips: filter the sample, explore mobility patterns, and interpret results.",
            "filters_header": "Dashboard filters",
            "f_dates": "Pickup dates",
            "f_hours": "Pickup hour range",
            "f_weekdays": "Days of week",
            "f_distance": "Trip distance (miles)",
            "f_points": "Points on map",
            "empty_selection": "No records match these filters. Widen the hour, date, day or distance selection.",
            "kpi_selected": "Selected trips",
            "kpi_avg_distance": "Avg. distance",
            "kpi_median_distance": "Median distance",
            "kpi_avg_duration": "Avg. duration",
            "kpi_median_speed": "Median speed",
            "selection_caption": "{sel:,} of {total:,} valid trips selected; {excluded:,} raw records excluded during cleaning.",
            "tabs": ["⏰ Time & demand", "📏 Distance & duration", "📍 Pickup geography"],
            "hourly_title": "Pickups by recorded hour",
            "hourly_x": "Pickup hour", "hourly_y": "Trips",
            "weekday_title": "Pickups by weekday",
            "weekday_x": "Weekday", "weekday_y": "Trips",
            "tab1_info": "Counts reflect the **sample and filters**, not citywide taxi trip totals. A weekday with more records may simply be better represented in the sample.",
            "hist_title": "Trip distance distribution (≤99th percentile)",
            "hist_x": "Distance (miles)",
            "hist_caption": "Clipping applies only to the displayed histogram, not KPIs or filters.",
            "speed_title": "Median implied speed by pickup hour",
            "speed_x": "Pickup hour", "speed_y": "Median speed (mph)",
            "scatter_title": "Trip duration vs. distance (sample)",
            "scatter_x": "Distance (miles)", "scatter_y": "Duration (min)", "scatter_color": "Hour",
            "scatter_caption": "Longer trips often take longer, but differences in duration alone cannot establish congestion or its causes.",
            "geo_subheader": "Taxi pickup locations",
            "geo_title": "Pickup locations ({n:,} sampled trips)",
            "geo_caption": "The displayed points are a reproducible random sample. Visible clusters indicate observed pickup concentration, not population-adjusted demand.",
            "insights_header": "🧠 Business insights for your selected filters",
            "insight_peak": "**Peak hour:** {hour}:00 has the most selected pickups. Staffing decisions should be based on a longer, representative period before operational use.",
            "insight_short": "**Short trips:** {pct:.1f}% of selected trips are **2 miles or less**, suggesting how much the sample is weighted toward shorter journeys.",
            "insight_corr": "**Distance and duration:** Pearson correlation = **{corr}**; interpretation requires caution because route, timing and weather may also affect duration.",
            "insight_spatial": "**Spatial usage:** Inspect the pickup map for observed clusters; airport or borough-level assertions require separate location validation.",
            "download_filtered": "Download filtered records as CSV",
            "footer": "Educational analysis only · Not a real-time view of NYC taxi demand.",
            "corr_undefined": "not defined",
        },
        "quality": {
            "title": "🧹 Data Quality & Preparation",
            "m_raw": "Raw rows", "m_valid": "Valid rows", "m_excluded": "Rows excluded",
            "m_excluded_delta": "{pct:.1%} of raw data",
            "missing_subheader": "Missing values in raw dataset",
            "missing_chart_title": "Missing data by column (top 15)",
            "missing_y": "Missing (%)", "missing_x": "Source field",
            "validation_subheader": "Validation rules",
            "validation_caption": "Each 'Records passing' count is independent. Do not add the excluded counts: individual records may fail several rules.",
            "sample_subheader": "Sample of cleaned rows",
            "download_csv": "Download cleaned data (CSV)",
            "checks": {
                "valid_time": "Valid timestamps and pickup hour",
                "distance_range": "Distance (0.01–100 miles)",
                "duration_range": "Duration (0.5–240 minutes)",
                "location_box": "Pickup within NYC bounding box",
                "speed_range": "Average speed (0.1–80 mph)",
                "all_passed": "All checks passed",
            },
            "col_check": "Check", "col_passing": "Records passing",
        },
        "cv": {"title": "👤 Curriculum Vitae"},
        "about": {
            "title": "ℹ️ Project & Methodology",
            "body": """### Goal
Explore **when**, **where** and **how far** NYC taxi trips occur, using interactive charts and useful business indicators.

### Dataset
[Kepler.gl taxi trips sample](https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv). The dataset is downloaded at runtime and cached for one day.

### Preparation
- Parse pickup and drop-off times; derive duration, hour, weekday and date.
- Exclude trips with missing/invalid timestamps, distances outside **0.01–100 miles**, durations outside **0.5–240 minutes**, pickup coordinates outside a broad NYC bounding box, and estimated speeds outside **0.1–80 mph**.
- The geographic bounding box is an **approximation**, not an official NYC administrative boundary.

### Interpretation warnings
- This sample may not represent all dates or all NYC taxis, so observed peaks are **sample-specific**.
- The pickup hour is read as recorded in the source string; its exact time-zone semantics are unverified.
- Distance is reported in **miles**. Implied speed is distance divided by trip duration, **not** a direct traffic sensor.
- High pickup density does not by itself prove where all NYC demand is greatest.
- The map uses a reproducible subset to keep the interface responsive.

### How to reproduce
Install `requirements.txt`, run `streamlit run app.py`, and use the sidebar filters. The notebook version can be kept in the same GitHub repository.
""",
        },
    },
}

st.set_page_config(page_title="NYC Taxi Explorer | KARAKOZIAN", page_icon="🚕", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>
.block-container{padding-top:2rem;max-width:1450px}
[data-testid="stMetric"]{background:#F4F7FB;border:1px solid #E1E7EF;border-radius:12px;padding:14px}
[data-testid="stMetricLabel"]{color:#42546A}
[data-testid="stMetricValue"]{color:#16202C}
small,.small-note{color:#58687A}
</style>""", unsafe_allow_html=True)

if "lang" not in st.session_state:
    st.session_state.lang = "fr"


@st.cache_data(ttl=86400, show_spinner=False)
def load_raw() -> pd.DataFrame:
    return pd.read_csv(DATA_URL)


@st.cache_data(show_spinner=False)
def clean_data(source: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    required = ["tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_distance", "pickup_latitude", "pickup_longitude"]
    absent = [x for x in required if x not in source.columns]
    if absent:
        raise ValueError(f"Dataset schema changed; required columns missing: {', '.join(absent)}")
    df = source.copy()
    # Preserve the clock hour as represented in the original pickup timestamp.
    clock = pd.to_datetime(df["tpep_pickup_datetime"].astype("string").str.slice(0, 19), errors="coerce")
    df["hour"] = clock.dt.hour
    df["weekday"] = clock.dt.day_name()
    df["date"] = clock.dt.date
    df["pickup_dt"] = pd.to_datetime(df["tpep_pickup_datetime"], errors="coerce", utc=True)
    df["dropoff_dt"] = pd.to_datetime(df["tpep_dropoff_datetime"], errors="coerce", utc=True)
    df["duration_min"] = (df["dropoff_dt"] - df["pickup_dt"]).dt.total_seconds() / 60
    for field in ["trip_distance", "pickup_latitude", "pickup_longitude", "duration_min"]:
        df[field] = pd.to_numeric(df[field], errors="coerce")

    date_valid = df["pickup_dt"].notna() & df["dropoff_dt"].notna() & df["hour"].notna()
    distance_valid = df["trip_distance"].between(0.01, 100)
    duration_valid = df["duration_min"].between(0.5, 240)
    location_valid = df["pickup_latitude"].between(40.45, 40.95) & df["pickup_longitude"].between(-74.30, -73.65)
    base_valid = date_valid & distance_valid & duration_valid & location_valid
    df["speed_mph"] = df["trip_distance"] / (df["duration_min"] / 60)
    speed_valid = df["speed_mph"].between(0.1, 80)
    clean = df.loc[base_valid & speed_valid].copy()
    stats = pd.DataFrame({
        "CheckKey": CHECK_KEYS,
        "Records passing": [int(date_valid.sum()), int(distance_valid.sum()), int(duration_valid.sum()), int(location_valid.sum()), int(speed_valid.sum()), len(clean)],
    })
    return clean, stats


def sample_for_plot(df: pd.DataFrame, n: int) -> pd.DataFrame:
    return df.sample(n=min(n, len(df)), random_state=42)


def graph(fig, filename: str, download_label: str) -> None:
    fig.update_layout(template="plotly_white", margin=dict(l=15, r=15, t=55, b=15))
    st.plotly_chart(fig, use_container_width=True)
    st.download_button(download_label, data=fig.to_html(full_html=True, include_plotlyjs=True), file_name=filename, mime="text/html", key=filename)


with st.sidebar:
    flag_fr, flag_en = st.columns(2)
    if flag_fr.button("🇫🇷 FR", use_container_width=True, type=("primary" if st.session_state.lang == "fr" else "secondary")):
        st.session_state.lang = "fr"
        st.rerun()
    if flag_en.button("🇬🇧 EN", use_container_width=True, type=("primary" if st.session_state.lang == "en" else "secondary")):
        st.session_state.lang = "en"
        st.rerun()

lang = st.session_state.lang
t = T[lang]
weekday_label = WEEKDAY_LABELS[lang]

with st.sidebar:
    st.title(t["app_title"])
    st.caption(t["sidebar_caption"])
    page = st.radio(t["pages_label"], options=["dashboard", "quality", "cv", "about"], format_func=lambda k: t["nav"][k], key="nav_page")
    st.divider()
    st.caption(t["source_caption"])

if page == "cv":
    cv = CV_CONTENT[lang]
    st.title(t["cv"]["title"])

    head_photo, head_text = st.columns([1, 4])
    photo_path = CV_DIR / "photo.png"
    if photo_path.exists():
        head_photo.image(str(photo_path), width=140)
    with head_text:
        st.header("Varoujan KARAKOZIAN")
        st.write(f"**{cv['role']}**")
        st.caption(cv["contact"])
        pdf_path = CV_DIR / cv["pdf_file"]
        if pdf_path.exists():
            st.download_button(cv["download_label"], data=pdf_path.read_bytes(), file_name=cv["pdf_file"], mime="application/pdf")

    st.divider()
    main_col, side_col = st.columns([2, 1])

    with main_col:
        st.subheader(cv["profile_header"])
        st.markdown(cv["profile"])

        st.subheader(cv["education_header"])
        for title, place, dates, note in cv["education"]:
            line = f"**{title}**  \n{place}" + (f", *{dates}*" if dates else "")
            st.markdown(line)
            if note:
                st.caption(note)

        st.subheader(cv["experience_header"])
        for job in cv["experience"]:
            st.markdown(f"**{job['title']}**  \n{job['place']}, *{job['dates']}*")
            for b in job["bullets"]:
                st.markdown(f"- {b}")

        st.subheader(cv["projects_header"])
        for title, dates, desc in cv["projects_recent"]:
            st.markdown(f"**{title}** ({dates})")
            st.markdown(f"- {desc}")
        st.markdown(f"**{cv['projects_earlier_label']}:** {cv['projects_earlier']}")

    with side_col:
        st.subheader(cv["skills_header"])
        for cat, items in cv["skills"]:
            st.markdown(f"**{cat}**")
            for it in items:
                st.markdown(f"- {it}")

        st.subheader(cv["languages_header"])
        for lg in cv["languages"]:
            st.markdown(f"- {lg}")

        st.subheader(cv["hobbies_header"])
        for h in cv["hobbies"]:
            st.markdown(f"- {h}")

    st.stop()

if page == "about":
    st.title(t["about"]["title"])
    st.markdown(t["about"]["body"])
    st.stop()

try:
    with st.spinner(t["loading_raw"]):
        raw = load_raw()
    with st.spinner(t["loading_clean"]):
        df, quality = clean_data(raw)
except Exception as exc:
    st.error(t["load_error_title"].format(exc=exc))
    st.info(t["load_error_hint"])
    st.stop()

if df.empty:
    st.error(t["empty_after_clean"])
    st.stop()

if page == "quality":
    q = t["quality"]
    st.title(q["title"])
    a, b, c = st.columns(3)
    a.metric(q["m_raw"], f"{len(raw):,}")
    b.metric(q["m_valid"], f"{len(df):,}")
    c.metric(q["m_excluded"], f"{len(raw)-len(df):,}", q["m_excluded_delta"].format(pct=(len(raw)-len(df))/len(raw)), delta_color="off")

    st.subheader(q["missing_subheader"])
    missing = pd.DataFrame({"field": raw.columns, "missing_count": raw.isna().sum().values, "missing_pct": (raw.isna().mean()*100).round(2).values}).sort_values("missing_pct", ascending=False)
    st.dataframe(missing, use_container_width=True, hide_index=True)
    fig = px.bar(missing.head(15), x="field", y="missing_pct", title=q["missing_chart_title"], labels={"missing_pct": q["missing_y"], "field": q["missing_x"]})
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(q["validation_subheader"])
    quality_display = quality.copy()
    quality_display[q["col_check"]] = quality_display["CheckKey"].map(q["checks"])
    quality_display = quality_display[[q["col_check"], "Records passing"]].rename(columns={"Records passing": q["col_passing"]})
    st.dataframe(quality_display, use_container_width=True, hide_index=True)
    st.caption(q["validation_caption"])

    st.subheader(q["sample_subheader"])
    st.dataframe(df[["date", "hour", "weekday", "trip_distance", "duration_min", "speed_mph", "pickup_latitude", "pickup_longitude"]].head(100), use_container_width=True)
    st.download_button(q["download_csv"], df.to_csv(index=False).encode("utf-8"), "nyc_taxi_cleaned.csv", "text/csv")
    st.stop()

# Dashboard
d = t["dashboard"]
st.title(d["title"])
st.caption(d["caption"])

with st.sidebar:
    st.subheader(d["filters_header"])
    dmin, dmax = min(df["date"]), max(df["date"])
    date_range = st.date_input(d["f_dates"], value=(dmin, dmax), min_value=dmin, max_value=dmax, key="filter_dates")
    hours = st.slider(d["f_hours"], 0, 23, (0, 23), key="filter_hours")
    weekdays = st.multiselect(d["f_weekdays"], WEEKDAYS, default=WEEKDAYS, format_func=lambda day: weekday_label[day], key="filter_weekdays")
    trip_range = st.slider(d["f_distance"], 0.0, 100.0, (0.0, 100.0), step=0.5, key="filter_distance")
    max_points = st.slider(d["f_points"], 500, 6000, 3000, step=500, key="filter_points")

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start, end = date_range
else:
    start, end = dmin, dmax
selection = df.loc[
    df["date"].between(start, end)
    & df["hour"].between(*hours)
    & df["weekday"].isin(weekdays)
    & df["trip_distance"].between(*trip_range)
].copy()

if selection.empty:
    st.warning(d["empty_selection"])
    st.stop()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric(d["kpi_selected"], f"{len(selection):,}")
k2.metric(d["kpi_avg_distance"], f"{selection['trip_distance'].mean():.2f} mi")
k3.metric(d["kpi_median_distance"], f"{selection['trip_distance'].median():.2f} mi")
k4.metric(d["kpi_avg_duration"], f"{selection['duration_min'].mean():.1f} min")
k5.metric(d["kpi_median_speed"], f"{selection['speed_mph'].median():.1f} mph")
st.caption(d["selection_caption"].format(sel=len(selection), total=len(df), excluded=len(raw)-len(df)))

tab1, tab2, tab3 = st.tabs(d["tabs"])
with tab1:
    left, right = st.columns(2)
    hourly = selection.groupby("hour").size().reindex(range(24), fill_value=0).rename_axis("hour").reset_index(name="trips")
    with left:
        fig = px.bar(hourly, x="hour", y="trips", title=d["hourly_title"], labels={"hour": d["hourly_x"], "trips": d["hourly_y"]})
        graph(fig, "hourly_demand.html", t["graph_download"])
    with right:
        counts = selection["weekday"].value_counts().reindex(WEEKDAYS, fill_value=0).rename_axis("weekday").reset_index(name="trips")
        counts["weekday_label"] = counts["weekday"].map(weekday_label)
        order = [weekday_label[day] for day in WEEKDAYS]
        fig = px.bar(counts, x="weekday_label", y="trips", title=d["weekday_title"], labels={"weekday_label": d["weekday_x"], "trips": d["weekday_y"]}, category_orders={"weekday_label": order})
        graph(fig, "weekday_demand.html", t["graph_download"])
    st.info(d["tab1_info"])

with tab2:
    left, right = st.columns(2)
    with left:
        cap = selection["trip_distance"].quantile(.99)
        plot = selection.loc[selection["trip_distance"] <= cap]
        fig = px.histogram(plot, x="trip_distance", nbins=45, title=d["hist_title"], labels={"trip_distance": d["hist_x"]})
        graph(fig, "trip_distance_histogram.html", t["graph_download"])
        st.caption(d["hist_caption"])
    with right:
        by_hour = selection.groupby("hour")["speed_mph"].median().reindex(range(24)).rename_axis("hour").reset_index(name="median_speed_mph")
        fig = px.line(by_hour, x="hour", y="median_speed_mph", markers=True, title=d["speed_title"], labels={"hour": d["speed_x"], "median_speed_mph": d["speed_y"]})
        graph(fig, "speed_by_hour.html", t["graph_download"])
    scatter_df = sample_for_plot(selection, 5000)
    fig = px.scatter(scatter_df, x="trip_distance", y="duration_min", color="hour", hover_data=["weekday", "speed_mph"], opacity=.55, title=d["scatter_title"], labels={"trip_distance": d["scatter_x"], "duration_min": d["scatter_y"], "hour": d["scatter_color"]})
    graph(fig, "duration_vs_distance.html", t["graph_download"])
    st.caption(d["scatter_caption"])

with tab3:
    st.subheader(d["geo_subheader"])
    geo = selection.loc[selection["pickup_latitude"].between(40.4, 41) & selection["pickup_longitude"].between(-74.3, -73.6)]
    geo = sample_for_plot(geo, max_points)
    fig = px.scatter_map(geo, lat="pickup_latitude", lon="pickup_longitude", color="hour", opacity=.58, zoom=9.5, height=590, map_style="carto-positron", hover_data={"trip_distance": ":.2f", "duration_min": ":.1f", "weekday": True, "pickup_latitude": False, "pickup_longitude": False}, title=d["geo_title"].format(n=len(geo)))
    fig.update_layout(map=dict(center=dict(lat=40.73, lon=-73.95)))
    graph(fig, "pickup_map.html", t["graph_download"])
    st.caption(d["geo_caption"])

st.subheader(d["insights_header"])
peak_hour = int(selection["hour"].value_counts().idxmax())
short_pct = 100*selection["trip_distance"].le(2).mean()
corr = selection[["trip_distance", "duration_min"]].corr().iloc[0, 1]
corr_description = f"{corr:.2f}" if pd.notna(corr) else d["corr_undefined"]
st.markdown(f"""
- {d['insight_peak'].format(hour=f"{peak_hour:02d}")}
- {d['insight_short'].format(pct=short_pct)}
- {d['insight_corr'].format(corr=corr_description)}
- {d['insight_spatial']}
""")
st.download_button(d["download_filtered"], selection.to_csv(index=False).encode("utf-8"), "nyc_taxi_filtered.csv", "text/csv")
st.caption(d["footer"])
