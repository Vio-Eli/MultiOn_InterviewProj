from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
import io
import os
from api import process_query
from models.multion_init import init_multion
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles

import dotenv
dotenv.load_dotenv()

app = FastAPI()
multion = init_multion()

# Mount the static files directory to serve HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')


@app.post("/query/")
async def search_text(description: str = Form(...), file: UploadFile = File(None)):
    if file:
        image = await file.read()
        with open("static/image.jpg", "wb") as f:
            f.write(image)
        image = "static/image.jpg"
    else:
        image = None
    result = process_query(description, image, multion)
    return JSONResponse(content={"results": result})

if __name__ == "__main__":
    uvicorn.run(app)
