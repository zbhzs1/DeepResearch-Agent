from langstudio.core import tool
from dataclasses import dataclass
import json, re

@dataclass
class Result:
    output1: list[str]
    step_num: int
    plan: str

def remove_thinking_tags(content: str) -> str:
    if not content:
        return content
    think_pattern = r".*?"
    cleaned_content = re.sub(think_pattern, "", content, flags=re.DOTALL)
    return cleaned_content.strip()

def extract_json_from_markdown(content: str) -> str:
    json_pattern = r"```(?:json)?\s*\n?(.*?)\n?```"
    match = re.search(json_pattern, content, flags=re.DOTALL)
    if match:
        return match.group(1).strip()
    return content

@tool
def invoke(plan_str: str) -> Result:
    fallback_steps = ["open source hardware cellular automata inspired", "RepRap Adrian Bowyer commercial entity"]
    fallback_plan_str = json.dumps({"rationale": "Fallback due to parse error", "sub_questions": fallback_steps})
    fallback_result = Result(output1=fallback_steps, step_num=len(fallback_steps) - 1, plan=fallback_plan_str)
    if not plan_str or not plan_str.strip():
        return fallback_result
    cleaned_str = remove_thinking_tags(plan_str)
    cleaned_str = extract_json_from_markdown(cleaned_str)
    try:
        start_idx = cleaned_str.find('{')
        end_idx = cleaned_str.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned_str = cleaned_str[start_idx:end_idx+1]
        plan = json.loads(cleaned_str)
        steps = plan.get("sub_questions", [])
        if not steps or not isinstance(steps, list):
            return fallback_result
        return Result(output1=steps, step_num=len(steps) - 1, plan=json.dumps(plan))
    except Exception as e:
        return fallback_result