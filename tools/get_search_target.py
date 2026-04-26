from langstudio.core import tool
from dataclasses import dataclass

@dataclass
class Result:
    output1: str

@tool
def invoke(input1: list[str], index: int) -> Result:
    return Result(output1=input1[index])