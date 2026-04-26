import requests
import time
from langstudio.core import tool
from dataclasses import dataclass

@dataclass
class Result:
    search_results: str

@tool
def invoke(query: str) -> Result:
    api_key = "" 
    if not query:
        return Result(search_results="未找到相关搜索结果，请尝试更换搜索关键词。")
    url = "https://cloud-iqs.aliyuncs.com/search/unified"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "engineType": "Generic", 
        "contents": {
            "mainText": False,
            "markdownText": False,
            "summary": False, 
            "rerankScore": True
        }
    }
    for delay in[1, 2, 3]:
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                page_items = data.get("pageItems", [])
                snippets =[]
                for i, item in enumerate(page_items[:5]):
                    title = item.get("title", "")
                    snippet = item.get("snippet", "")
                    if title or snippet:
                        snippets.append(f"[{i+1}] 标题: {title}\n摘要: {snippet}\n")
                if not snippets:
                    return Result(search_results="未找到相关搜索结果，请尝试更换搜索关键词。")
                return Result(search_results="\n".join(snippets))
            elif response.status_code == 429:
                time.sleep(delay)
                continue
            else:
                return Result(search_results=f"搜索工具调用失败，状态码: {response.status_code}, 报错详情: {response.text}")
        except Exception as e:
            time.sleep(delay)
            continue
    return Result(search_results="搜索工具连续调用失败或超时。")