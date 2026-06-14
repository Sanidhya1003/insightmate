import pandas as pd
import streamlit as st

from src.agent import explain_result_with_llm, route_question_with_llm
from src.analysis_tools import execute_tool
from src.config import APP_NAME, APP_VERSION


st.set_page_config(
    page_title=APP_NAME,
    page_icon="📊",
    layout="wide",
)


# -----------------------------
# Session state
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "df" not in st.session_state:
    st.session_state.df = None

if "dataset_name" not in st.session_state:
    st.session_state.dataset_name = None

if "analysis_log" not in st.session_state:
    st.session_state.analysis_log = []


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("📊 InsightMate AI")
st.sidebar.caption(APP_VERSION)

uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file",
    type=["csv"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Try these")

example_questions = [
    "Summarise this dataset",
    "What columns are in this dataset?",
    "Are there any missing values?",
    "Which region has the highest revenue?",
    "Show total revenue by category as a chart",
    "Find outliers in the numeric columns",
    "Give me 3 business insights from this dataset",
]

for q in example_questions:
    st.sidebar.code(q)

st.sidebar.markdown("---")

if st.sidebar.button("Clear chat"):
    st.session_state.messages = []
    st.session_state.analysis_log = []
    st.rerun()


# -----------------------------
# Header
# -----------------------------

st.title("📊 InsightMate AI")
st.caption("Agentic Data Analyst Chatbot — Version 2")


# -----------------------------
# Dataset upload
# -----------------------------

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.session_state.df = df
        st.session_state.dataset_name = uploaded_file.name

        st.success(f"CSV uploaded successfully: {uploaded_file.name}")

    except Exception as e:
        st.error(f"Could not read CSV file: {e}")


if st.session_state.df is None:
    st.info("Upload a CSV file to start chatting with your data.")
    st.stop()


df = st.session_state.df


# -----------------------------
# Dataset overview
# -----------------------------

with st.expander("Dataset preview", expanded=False):
    st.write(f"**Dataset:** {st.session_state.dataset_name}")
    st.write(f"**Rows:** {df.shape[0]}")
    st.write(f"**Columns:** {df.shape[1]}")
    st.dataframe(df.head(20), use_container_width=True)


# -----------------------------
# Analysis report export
# -----------------------------

def build_markdown_report() -> str:
    """
    Creates a simple markdown export of the chat and analysis log.
    """

    lines = [
        "# InsightMate AI Analysis Report",
        "",
        f"Dataset: {st.session_state.dataset_name}",
        f"Rows: {df.shape[0]}",
        f"Columns: {df.shape[1]}",
        "",
        "## Conversation",
        "",
    ]

    for msg in st.session_state.messages:
        role = msg["role"].title()
        content = msg["content"]
        lines.append(f"### {role}")
        lines.append(content)
        lines.append("")

    lines.append("## Agent Actions")
    lines.append("")

    for item in st.session_state.analysis_log:
        lines.append(f"### Question")
        lines.append(item.get("question", ""))
        lines.append("")
        lines.append("### Tool")
        lines.append(str(item.get("tool", "")))
        lines.append("")
        lines.append("### SQL")
        lines.append("```sql")
        lines.append(str(item.get("sql", "")))
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


if st.session_state.messages:
    report_md = build_markdown_report()

    st.download_button(
        label="Download analysis report",
        data=report_md,
        file_name="insightmate_analysis_report.md",
        mime="text/markdown",
    )


# -----------------------------
# Existing chat messages
# -----------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# Chat input
# -----------------------------

question = st.chat_input("Ask a question about your dataset...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Agent is choosing the right tool..."):
                plan = route_question_with_llm(question, df)

            with st.expander("Agent decision"):
                st.json(plan)

            with st.spinner("Running analysis tool..."):
                result = execute_tool(plan, df)

            if result.get("sql"):
                with st.expander("SQL used"):
                    st.code(result["sql"], language="sql")

            if isinstance(result.get("dataframe"), pd.DataFrame):
                st.dataframe(result["dataframe"], use_container_width=True)

            if result.get("chart") is not None:
                st.plotly_chart(result["chart"], use_container_width=True)

            with st.spinner("Preparing final explanation..."):
                answer = explain_result_with_llm(question, plan, result)

            st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
            })

            st.session_state.analysis_log.append({
                "question": question,
                "tool": plan.get("tool"),
                "sql": plan.get("sql"),
            })

        except Exception as e:
            error_message = f"Something went wrong: {e}"
            st.error(error_message)

            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message,
            })