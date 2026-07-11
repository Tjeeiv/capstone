# SmartRetail 360 — Analytics & AI Support Platform

An end-to-end data and AI intelligence platform for e-commerce businesses. Built as a capstone project covering data engineering, machine learning, generative AI, and API development.

---

## Architecture Overview

```
Kaggle (Olist Brazilian E-Commerce Dataset)
                    ↓
     Snowflake Cloud Data Warehouse
     ┌──────────────────────────────┐
     │  BRONZE  →  SILVER  →  GOLD  │   ← Medallion Architecture
     └──────────────────────────────┘
              ↓                ↓
       ML Pipeline       Review Knowledge Base
     (Linear Regression)  (FAISS + Embeddings)
              ↓                ↓
         FastAPI Backend (port 8000)
         ├── POST /predict-sales
         └── POST /ask-assistant (RAG)
                      ↓
         Streamlit Frontend (port 8501)
         ├── Business Dashboard View
         └── AI Assistant Chat View
```

---

## Project Structure

```
├── app.py                        # Streamlit entry point / Home page
├── Pages/                        # Streamlit navigation pages
│   ├── 1_Get_Dataset.py          # Kaggle download → Snowflake Bronze
│   ├── 2_Build_Data.py           # Bronze → Silver → Gold pipeline
│   ├── 3_Visualization.py        # EDA charts
│   ├── 4_ML.py                   # Model training + evaluation
│   ├── 5_Knowledge_Base.py       # Embeddings + FAISS index builder
│   ├── 6_Business_Dashboard.py   # Charts + revenue prediction form
│   └── 7_AI_Assistant.py         # Conversational review chat
├── Services/                     # Business logic layer
│   ├── snowflakeconnector.py     # Snowflake connection factory
│   ├── datasetservice.py         # Kaggle download + Bronze upload
│   ├── datacleanservice.py       # Silver + Gold transformations
│   ├── visualizeservice.py       # Chart generation functions
│   ├── mlservice.py              # Feature engineering + model training
│   ├── vectorembSem.py           # Embeddings + FAISS index + search
│   └── ragservice.py             # RAG pipeline (retrieve + generate)
├── api/                          # FastAPI backend
│   ├── main.py                   # App entry point + router registration
│   ├── routes/
│   │   ├── predict.py            # /predict-sales endpoint
│   │   └── assistant.py          # /ask-assistant endpoint
│   └── models/
│       └── schemas.py            # Pydantic input/output schemas
├── appsettings.json              # Non-sensitive config (dataset name, paths)
├── requirements.txt              # Python dependencies
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data Source | Kaggle — Olist Brazilian E-Commerce Dataset |
| Cloud Data Warehouse | Snowflake (Bronze / Silver / Gold schemas) |
| Data Processing | Python, Pandas |
| Machine Learning | Scikit-learn (Linear Regression, StandardScaler) |
| Embeddings | Hugging Face `paraphrase-multilingual-MiniLM-L12-v2` |
| Vector Store | FAISS (local, Facebook AI Similarity Search) |
| LLM | Google `flan-t5-base` (local, free, no API cost) |
| Backend API | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Version Control | Git + GitHub |

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- A Snowflake account (free trial works)
- A Kaggle account with API token

### 1. Clone the repository
```bash
git clone https://github.com/Tjeeiv/capstone.git
cd capstone
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the project root (never commit this file):
```
KaggleAPIKey=your_kaggle_api_token

SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
```

### 4. Set up Snowflake schemas
Run this once in your Snowflake worksheet:
```sql
CREATE SCHEMA IF NOT EXISTS BRONZE;
CREATE SCHEMA IF NOT EXISTS SILVER;
CREATE SCHEMA IF NOT EXISTS GOLD;
CREATE STAGE IF NOT EXISTS BRONZE.CAPSTONERAWDATAFILES;
```

### 5. Run the data pipeline (in order)
Start the Streamlit app:
```bash
streamlit run app.py
```

Then follow these steps from the sidebar:
1. **Get Dataset** — downloads Olist data from Kaggle, uploads raw files to Snowflake Bronze stage
2. **Build Data** — runs Bronze → Silver (cleaning) → Gold (business-ready joins) pipeline
3. **Visualization** — view EDA charts (confirm data is correct before modeling)
4. **ML** — trains Linear Regression model, saves `.pkl` files to `./models/`
5. **Knowledge Base** — generates multilingual embeddings, builds FAISS index in `./vectorstore/`

### 6. Start the FastAPI backend (separate terminal)
```bash
python -m uvicorn api.main:app --reload --port 8000
```

Verify it's running: `http://localhost:8000`
View auto-generated API docs: `http://localhost:8000/docs`

### 7. Use the application
With both servers running, navigate in the Streamlit sidebar to:
- **Business Dashboard** — view charts and get revenue predictions
- **AI Assistant** — chat with the review assistant

---

## API Reference

### `POST /predict-sales`
Predicts next month's total revenue based on current month's business metrics.

**Request body:**
```json
{
  "monthrev": 1200000.0,
  "monthorderitemcount": 1500,
  "monthordercount": 850,
  "monthavgrevenue": 800.0,
  "monthnumber": 9
}
```

**Response:**
```json
{
  "predicted_revenue": 1350000.0
}
```

---

### `POST /ask-assistant`
Accepts a natural language question, retrieves semantically relevant customer reviews via FAISS, and returns an AI-generated answer using a local LLM.

**Request body:**
```json
{
  "question": "What do customers say about delivery?"
}
```

**Response:**
```json
{
  "answer": "Customers are generally satisfied with delivery times and service.",
  "sources": [
    "Tudo certo com a compra e entrega",
    "Otima compra e entrega.",
    "Satisfeito com a entrega... atendimento e produto"
  ]
}
```

---

## Milestones

| Milestone | Description | Status |
|---|---|---|
| 1 — Data Pipeline | Kaggle → Snowflake medallion architecture (Bronze/Silver/Gold) | ✅ Complete |
| 2 — EDA & ML | 3 visualizations + feature engineering + Linear Regression | ✅ Complete |
| 3 — Vector Embeddings | Multilingual embeddings + FAISS semantic search | ✅ Complete |
| 4 — Backend API | FastAPI with `/predict-sales` and `/ask-assistant` endpoints | ✅ Complete |
| 5 — Streamlit UI | Business Dashboard + AI Assistant chat interface | ✅ Complete |

---

## Design Decisions & Notes

### Why Snowflake instead of SQLite/MongoDB?
The project specification suggested SQLite and MongoDB. This implementation uses Snowflake with a medallion architecture instead — a real-world enterprise data engineering pattern where raw data lands in Bronze, cleaned data moves to Silver, and business-ready aggregations sit in Gold. This is more scalable and production-ready, and demonstrates cloud data engineering skills beyond the minimum requirements.

### Why multilingual embeddings?
The Olist dataset contains customer reviews in Portuguese. Rather than running a separate translation pipeline (which adds cost and complexity), this project uses `paraphrase-multilingual-MiniLM-L12-v2` — a Hugging Face model trained on 50+ languages. This means English queries correctly retrieve semantically matching Portuguese reviews without any translation step.

### Note on model performance
The Linear Regression model shows a negative R² score on the test set. This is a known limitation: the model was trained on Olist's rapid growth phase (2016–2017), while the test period (2018) shows revenue plateauing. Linear Regression assumes one consistent trend across all data — it cannot detect when the underlying pattern changes. A time-series model such as Prophet or ARIMA would be more appropriate for this dataset in a production setting.

---

## Author
Built by Siddhu as part of the SmartRetail 360 capstone project.