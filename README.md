# InsightMate AI

InsightMate AI is an agentic data analyst chatbot that allows users to upload CSV datasets and ask questions in natural language.

The system uses an LLM through the OpenAI API to decide which analysis tool to use, then runs actual data operations using Pandas and DuckDB.

## Features

- CSV upload
- Natural language data questions
- Agentic tool selection
- Safe SQL query generation
- Dataset profiling
- Missing value detection
- Outlier detection
- Chart generation
- Business insight generation

## Tech Stack

- Python
- Streamlit
- OpenAI API
- Pandas
- DuckDB
- Plotly

## How to Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py