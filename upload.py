from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path

app = FastAPI()

# Define the upload folder
upload_folder = Path("uploads")
upload_folder.mkdir(exist_ok=True)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Save the file to the upload folder
    file_path = upload_folder / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "content_type": file.content_type}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
