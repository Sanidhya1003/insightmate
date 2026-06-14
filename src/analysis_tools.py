from typing import Any, Dict, Optional

import pandas as pd
import plotly.express as px

from src.data_utils import (
    missing_values_report,
    outlier_report,
    profile_data,
)
from src.sql_utils import run_sql_query


def create_chart(
    result_df: pd.DataFrame,
    chart_type: str,
    x: str,
    y: Optional[str],
):
    """
    Creates a Plotly chart from SQL result data.
    """

    if result_df.empty:
        return None

    if not x or x not in result_df.columns:
        return None

    if y and y not in result_df.columns:
        y = None

    if chart_type == "line":
        return px.line(result_df, x=x, y=y)

    if chart_type == "scatter":
        return px.scatter(result_df, x=x, y=y)

    return px.bar(result_df, x=x, y=y)


def execute_tool(plan: Dict[str, Any], df: pd.DataFrame) -> Dict[str, Any]:
    """
    Executes the tool selected by the agent router.
    """

    tool = plan.get("tool")

    result = {
        "tool": tool,
        "text": "",
        "dataframe": None,
        "chart": None,
        "sql": plan.get("sql"),
    }

    if tool == "profile_data":
        text, table = profile_data(df)
        result["text"] = text
        result["dataframe"] = table

    elif tool == "missing_values":
        text, table = missing_values_report(df)
        result["text"] = text
        result["dataframe"] = table

    elif tool == "outliers":
        text, table = outlier_report(df)
        result["text"] = text
        result["dataframe"] = table

    elif tool == "run_sql":
        sql = plan.get("sql")
        table = run_sql_query(df, sql)
        result["text"] = "SQL query executed successfully."
        result["dataframe"] = table

    elif tool == "chart":
        sql = plan.get("sql")
        table = run_sql_query(df, sql)

        fig = create_chart(
            table,
            plan.get("chart_type") or "bar",
            plan.get("x"),
            plan.get("y"),
        )

        result["text"] = "Chart data prepared successfully."
        result["dataframe"] = table
        result["chart"] = fig

    elif tool == "business_summary":
        text, profile_table = profile_data(df)
        missing_text, _ = missing_values_report(df)
        outlier_text, _ = outlier_report(df)

        combined = f"""
{text}

{missing_text}

{outlier_text}
"""

        result["text"] = combined
        result["dataframe"] = profile_table

    elif tool == "chat":
        result["text"] = "This question does not require dataset analysis."

    else:
        raise ValueError(f"Unknown tool selected: {tool}")

    return result


def result_to_text(result: Dict[str, Any]) -> str:
    """
    Converts tool output into compact text for the final LLM explanation.
    """

    output = f"""
Tool used: {result.get("tool")}
Tool message: {result.get("text")}
SQL used: {result.get("sql")}
"""

    df = result.get("dataframe")

    if isinstance(df, pd.DataFrame):
        output += "\nResult table preview:\n"
        output += df.head(20).to_csv(index=False)

    return output