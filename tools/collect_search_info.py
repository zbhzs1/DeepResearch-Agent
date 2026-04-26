from langstudio.core import tool
from dataclasses import dataclass

@dataclass
class Result:
    content: str

@tool
def invoke(current: str, history: any) -> Result:
    c = str(current) if current is not None else ""
    if history is None or not isinstance(history, str):
        h = ""
    else:
        h = str(history)
    final_content = c if h == "" else h + ";;  \n" + c
    return Result(content=final_content)