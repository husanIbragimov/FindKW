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

    for item in raw_data:
        item["search_keywords"] = [kw.lower() for kw in item["keywords"]]

    data = raw_data


@app.get("/search")
def search(
    keyword: str = Query(None, description="Search keyword"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page (max 100)")
):
    keyword_lower = keyword.lower() if keyword else None

    # Filter data if keyword is provided
    if keyword_lower:
        filtered = [
            item for item in data
            if any(keyword_lower in kw for kw in item["search_keywords"])
        ]
    else:
        filtered = data

    total = len(filtered)
    start = (page - 1) * limit
    end = start + limit
    paginated_data = filtered[start:end]

    return JSONResponse(content={
        "page": page,
        "limit": limit,
        "total": total,
        "data": paginated_data
    })
