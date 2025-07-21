from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from pydantic import BaseModel

app=FastAPI()

items={
    1: {"name": "Laptop", "description": "A portable computer"},
    2: {"name": "phone", "description": "a smart phone for communication"},
    3: {"name": "tablet", "description": "a portable touch screen device"},
}

#pydanctic model
class Item(BaseModel):
    name:str
    description: str

#get endpoint with path parameter
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id in items:
        return items[item_id]
    raise HTTPException(status_code=404, detail="Item not found")

#get endpoit with query parameter
@app.get("/search/")
async def search_items(q: str = Query(..., min_length=3)):
    results = {id: item for id, item in items.items() if q.lower() in item["name"].lower()}
    if results:
        return results
    raise HTTPException(status_code=404, detail="No items found matching the query")

#post with request body
@app.post("/items/")
async def create_item(item: Item):
    item_id = max(items.keys()) + 1
    items[item_id] = item.dict()
    return {"item_id": item_id, "item": items[item_id]}

#file upload endpoint
@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type
    }


