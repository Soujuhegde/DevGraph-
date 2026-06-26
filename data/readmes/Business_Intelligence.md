# ⚡ Clarity AI: Intelligent Business Analyst

![Clarity AI Dashboard](https://img.shields.io/badge/Status-Active-brightgreen) ![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit) ![Groq](https://img.shields.io/badge/Groq-Llama%203.3-orange)

Clarity AI is an advanced, automated Business Intelligence platform built with a **FastAPI** backend and a highly customized, premium **Streamlit** frontend. 

It acts as your personal AI data analyst: ingesting raw business data, automatically cleaning it, performing anomaly detection and forecasting, and providing an interactive **"AI Copilot"** allowing you to query your database in plain English.

---

## 🚀 Key Features

- **Automated Data Pipeline & Cleaning:** Upload messy CSV files. The backend AI automatically infers data types, detects anomalies, and sanitizes the dataset before loading it into a live SQLite database.
- **Dynamic Real-Time Simulation:** A background engine intelligently samples from your uploaded historical data and simulates a live, real-time data stream that powers the live dashboard metrics.
- **Dynamic AI Copilot (Text-to-SQL):** Ask questions about your business metrics in plain English. Powered by LangChain and Groq's blazing fast Llama 3.3 (70B) model, the copilot translates your intent into SQL, runs it against the live database, and returns actionable insights.
- **Machine Learning Forecasting:** Utilizes Scikit-Learn's `LinearRegression` to detect trends across both historical and real-time streaming data, generating smoothed future projections.
- **Intelligent Anomaly Detection:** Employs `IsolationForest` algorithms to actively scan your data and highlight anomalous records, preventing outliers from skewing your insights.
- **Automated PDF Reports:** A reporting agent that dynamically detects your core KPIs and uses an LLM to draft professional executive summaries, exported directly to a clean PDF format.
- **Premium UI/UX:** A fully custom "Light Beige & Lime Green" glassmorphic design theme featuring custom CSS animations, overriding standard Streamlit limitations.

---

## 🏗️ Architecture & Technologies

- **Backend:** Python, FastAPI, Uvicorn, SQLite, SQLAlchemy
- **Data Engineering:** Pandas, Numpy
- **Machine Learning:** Scikit-Learn (`IsolationForest`, `LinearRegression`)
- **Generative AI:** LangChain, Groq API (Llama 3.3 70B)
- **Frontend:** Streamlit, Plotly Express, Custom CSS
- **Reporting:** FPDF

## 📂 Project Structure

```text
Business-Intelligence-Analyst/
├── src/
│   ├── backend/          
│   │   ├── agents/       # Specialized AI Agents (SQL, Cleaning, Report, Forecast, Anomaly)
│   │   ├── main.py       # FastAPI application and live generator thread
│   │   └── database.py   # SQLite connection and data loading
│   ├── frontend/         
│   │   ├── components/   # UI styling, sidebar, helpers
│   │   ├── pages_content/# Modular Streamlit pages
│   │   └── app.py        # Main Streamlit entrypoint
│   └── data/             # Uploaded and cleaned datasets, PDFs
├── .streamlit/           # Custom Streamlit configuration
├── requirements.txt      # Project dependencies
├── start_backend.ps1     # Helper script to launch backend
└── start_frontend.ps1    # Helper script to launch frontend
```

---

## 💻 Getting Started

### Prerequisites
- Python 3.9+
- A [Groq API Key](https://console.groq.com/) for the LLM features. Add it to a `.env` file in the root directory: `GROQ_API_KEY=your_key_here`

### Installation & Running

1. **Activate your virtual environment**:
   ```powershell
   .\.venv\Scripts\activate.ps1
   ```

2. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Start the Backend API**:
   The backend provides the API for data cleaning, forecasting, real-time simulation, and the Copilot LLM interface.
   ```powershell
   .\start_backend.ps1
   ```

4. **Start the Frontend Dashboard**:
   In a new terminal, launch the Streamlit app.
   ```powershell
   .\start_frontend.ps1
   ```

5. Open your browser and navigate to `http://localhost:8501`.