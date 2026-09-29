# InsightMate AI

InsightMate AI is an agentic data analyst chatbot that lets users upload CSV datasets and ask questions in natural language.

The application uses an LLM through the Groq API to route user questions to the correct analysis tool, then runs actual data operations using Pandas, DuckDB, and Plotly. It is designed as a practical AI/data product rather than a notebook-only ML project.

## Features

- Upload CSV datasets
- Ask natural-language questions about the data
- LLM-powered agentic tool routing
- Dataset profiling
- Missing value detection
- Outlier detection using the IQR method
- Safe SQL query generation and execution with DuckDB
- Chart generation using Plotly
- Business insight generation
- Chat-style Streamlit interface
- Agent decision visibility
- SQL query visibility
- Downloadable Markdown analysis report

## Example Questions

```text
Summarise this dataset
What columns are in this dataset?
Are there any missing values?
Which region has the highest revenue?
Show total revenue by category as a chart
Find outliers in the numeric columns
Give me 3 business insights from this dataset
```

## Tech Stack

- Python
- Streamlit
- Groq API
- Pandas
- DuckDB
- Plotly
- python-dotenv

## Project Structure

```text
insightmate/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── sample_data/
│   └── retail_sales.csv
│
└── src/
    ├── agent.py
    ├── analysis_tools.py
    ├── config.py
    ├── data_utils.py
    ├── llm_client.py
    ├── prompts.py
    └── sql_utils.py
```

## How It Works

1. The user uploads a CSV file.
2. The LLM receives the dataset schema, sample rows, and user question.
3. The agent router selects one tool:
   - dataset profile
   - missing value report
   - outlier detection
   - SQL analysis
   - chart generation
   - business summary
4. The selected Python tool runs the actual analysis.
5. The LLM explains the result in natural language.

## Safety

The SQL execution layer only allows read-only `SELECT` and `WITH` queries. It blocks unsafe operations such as `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, file access, and similar commands.

## Setup

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

Run the app:

```bash
streamlit run app.py
```

## Sample Dataset

A small sample retail dataset is included in:

```text
sample_data/retail_sales.csv
```

You can use it to test the chatbot quickly.

## Current Status

Version 2 is complete.

Implemented:

- modular project structure
- Streamlit user interface
- Groq LLM integration
- agentic routing
- safe SQL execution
- profiling, missing value, outlier, chart, and insight tools
- markdown report export

Planned:

- Docker-based deployment
- cloud-hosted live demo
- improved error handling
- richer chart selection
- advanced memory and report generation
