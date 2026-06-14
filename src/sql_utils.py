import re

import duckdb
import pandas as pd


def validate_sql(sql: str) -> str:
    """
    Allows only safe read-only SQL.
    """

    if not sql:
        raise ValueError("No SQL query was provided.")

    cleaned = sql.strip().rstrip(";")

    if not re.match(r"^(select|with)\b", cleaned, re.IGNORECASE):
        raise ValueError("Only SELECT queries are allowed.")

    blocked_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "copy",
        "pragma",
        "attach",
        "detach",
        "call",
        "execute",
        "read_csv",
        "read_parquet",
        "write_csv",
        "write_parquet",
    ]

    lowered = cleaned.lower()

    for keyword in blocked_keywords:
        if re.search(rf"\b{keyword}\b", lowered):
            raise ValueError(f"Blocked unsafe SQL keyword: {keyword}")

    return cleaned


def run_sql_query(df: pd.DataFrame, sql: str) -> pd.DataFrame:
    """
    Runs a safe SQL query against the uploaded dataframe using DuckDB.
    """

    safe_sql = validate_sql(sql)

    con = duckdb.connect(database=":memory:")
    con.register("data", df)

    result = con.execute(safe_sql).fetchdf()

    con.close()

    return result