from langstudio.core import tool
from dataclasses import dataclass
import json, re

@dataclass
class Result:
    enough_and_clear: str
    feedback: str
    question: str

def remove_thinking_tags(content: str) -> str:
    if not content:
        return content
    think_pattern = r".*?"
    cleaned_content = re.sub(think_pattern, "", content, flags=re.DOTALL)
    return cleaned_content.strip()

@tool
def invoke(plan_str: str) -> Result:
    plan_str = remove_thinking_tags(plan_str)
    if plan_str.startswith("```json"):
        plan_str = plan_str[7:-3]
    plan = json.loads(plan_str)
    enough_and_clear = plan.get("enough_and_clear")
    feedback = plan.get("feedback")
    question = plan.get("question")
    return Result(
        enough_and_clear=str(enough_and_clear),
        feedback=str(feedback),
        question=str(question),
    )