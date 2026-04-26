from langstudio.core import tool
import requests
import json
import time

@tool
def invoke(query: str) -> str:
    api_key = "" 
    if not query:
        return ""
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
    for delay in [1, 2, 3]:
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
            if response.status_code == 200:
                data = response.json()
                page_items = data.get("pageItems", [])
                snippets = []
                for item in page_items[:5]:
                    title = item.get("title", "")
                    snippet = item.get("snippet", "")
                    link = item.get("link", item.get("url", "")) 
                    if title or snippet:
                        snippets.append(f"标题: {title}\n链接: {link}\n摘要: {snippet}")
                return "\n\n".join(snippets) if snippets else "未找到相关结果"
            elif response.status_code == 429:
                time.sleep(delay)
                continue
            else:
                return f"IQS 搜索报错，状态码: {response.status_code}, 信息: {response.text}"
        except Exception as e:
            time.sleep(delay)
            continue
    return "搜索工具调用异常或超时"