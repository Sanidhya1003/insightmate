import json
import re
from typing import Any, Dict

import pandas as pd

from src.analysis_tools import result_to_text
from src.data_utils import get_dataset_context
from src.llm_client import call_llm
from src.prompts import EXPLAINER_SYSTEM_PROMPT, ROUTER_SYSTEM_PROMPT


def extract_json(text: str) -> Dict[str, Any]:
    """
    Extracts JSON from LLM output.
    This handles cases where the model accidentally wraps JSON in extra text.
    """

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            return json.loads(match.group(0))

        raise ValueError("Could not parse JSON from model response.")


def route_question_with_llm(question: str, df: pd.DataFrame) -> Dict[str, Any]:
    """
    Agent router.
    The LLM decides which analysis tool should handle the question.
    """

    dataset_context = get_dataset_context(df)

    user_prompt = f"""
Dataset context:
{dataset_context}

User question:
{question}
"""

    response_text = call_llm(
        system_prompt=ROUTER_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.1,
    )

    return extract_json(response_text)


def explain_result_with_llm(
    question: str,
    plan: Dict[str, Any],
    result: Dict[str, Any],
) -> str:
    """
    Final response generator.
    """

    tool_result_text = result_to_text(result)

    user_prompt = f"""
User question:
{question}

Agent plan:
{json.dumps(plan, indent=2)}

Tool result:
{tool_result_text}
"""

    return call_llm(
        system_prompt=EXPLAINER_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.2,
    )