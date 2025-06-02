from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import orjson

app = FastAPI()
data = []  # Global data store


@app.on_event("startup")
def load_json():
    global data
    with open("lugat_with_keywords.json", "rb") as f:
        raw_data = orjson.loads(f.read())

    # Har bir item uchun search_keywords degan lower case list qo‘shamiz
    for item in raw_data:
        item["search_keywords"] = [kw.lower() for kw in item["keywords"]]

    data = raw_data


@app.get("/search")
def search(keyword: str):
    keyword_lower = keyword.lower()

    results = [
        item for item in data
        if any(keyword_lower in kw for kw in item["search_keywords"])
    ]

    return JSONResponse(content=results)
