from langstudio.core import tool
from dataclasses import dataclass

@dataclass
class Result:
    output2: int

@tool
def invoke(input2: int) -> Result:
    return Result(output2=input2 + 1)