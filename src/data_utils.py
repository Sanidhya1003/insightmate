import pandas as pd


def get_dataset_context(df: pd.DataFrame) -> str:
    """
    Creates a compact dataset description for the LLM.
    We send schema + small sample, not the whole dataset.
    """

    schema_lines = []

    for col in df.columns:
        schema_lines.append(f"- {col}: {df[col].dtype}")

    sample = df.head(5).to_csv(index=False)

    return f"""
Dataset table name: data

Rows: {df.shape[0]}
Columns: {df.shape[1]}

Schema:
{chr(10).join(schema_lines)}

Sample rows:
{sample}
"""


def profile_data(df: pd.DataFrame):
    """
    Returns basic dataset profile.
    """

    summary = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(df[col].dtype) for col in df.columns],
        "missing_values": [int(df[col].isna().sum()) for col in df.columns],
        "unique_values": [int(df[col].nunique(dropna=True)) for col in df.columns],
    })

    text = f"""
Dataset profile:
- Rows: {df.shape[0]}
- Columns: {df.shape[1]}
- Numeric columns: {len(df.select_dtypes(include='number').columns)}
- Text/category columns: {len(df.select_dtypes(exclude='number').columns)}
"""

    return text, summary


def missing_values_report(df: pd.DataFrame):
    """
    Returns missing value report.
    """

    missing = df.isna().sum().reset_index()
    missing.columns = ["column", "missing_values"]
    missing["missing_percent"] = (missing["missing_values"] / len(df) * 100).round(2)
    missing = missing.sort_values("missing_values", ascending=False)

    total_missing = int(missing["missing_values"].sum())

    text = f"Total missing values found: {total_missing}"

    return text, missing


def outlier_report(df: pd.DataFrame):
    """
    Simple IQR-based outlier detection for numeric columns.
    """

    numeric_cols = df.select_dtypes(include="number").columns

    rows = []

    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        count = int(((df[col] < lower) | (df[col] > upper)).sum())

        rows.append({
            "column": col,
            "outlier_count": count,
            "outlier_percent": round(count / len(df) * 100, 2),
            "lower_bound": round(lower, 2),
            "upper_bound": round(upper, 2),
        })

    report = pd.DataFrame(rows).sort_values("outlier_count", ascending=False)

    text = "Outliers were detected using the IQR method for numeric columns."

    return text, report