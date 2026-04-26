from langstudio.core import tool
from dataclasses import dataclass

@dataclass
class Result:
  reference: str
  abstract: str

@tool
def invoke(input1: str) -> Result:
  reference = ""
  abstract = ""
  if not input1:
    return Result(reference="", abstract="")
  input_text = str(input1)
  ref_marker = "## 参考来源"
  if ref_marker in input_text:
    ref_start = input_text.find(ref_marker) + len(ref_marker)
    reference = input_text[ref_start:].strip()
  abstract_marker = "## 摘要"
  content_marker = "## 正文"
  if abstract_marker in input_text:
    abstract_start = input_text.find(abstract_marker) + len(abstract_marker)
    if content_marker in input_text:
      content_start = input_text.find(content_marker)
      abstract = input_text[abstract_start:content_start].strip()
    else:
      abstract = input_text[abstract_start:].strip()
  return Result(reference=reference.strip(), abstract=abstract.strip())