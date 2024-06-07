from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import uvicorn
from PIL import Image
import io
from api import process_query

import dotenv
dotenv.load_dotenv()

app = FastAPI()


@app.post("/query/")
async def search_text(description: str = Form(...), file: UploadFile = File(None)):
    if file:
        contents = await file.read()
        image = io.BytesIO(contents)
    else:
        image = None
    result = process_query(description, image)
    return JSONResponse(content={"results": result})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
