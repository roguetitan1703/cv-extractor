from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from zipfile import ZipFile
from fastapi.templating import Jinja2Templates
import os, sys, secrets, asyncio
import uuid
from shutil import make_archive
import uvicorn

project_root = os.getcwd()

# Local imports 
from scraper.scraper import Scraper
# Setting up the app
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class = HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/extract_data")
async def uploadfile(file: UploadFile):
    try:
        print(f"File: {file.filename}")
        file_path = f"{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        CVscraper = Scraper(log_file="main.log")
        extract_data = CVscraper.read_and_exctract_from_cvs(file_path,zip_file=True)
        
        if extract_data['status'] == 'error':
            
            return {
                "status": "error",
                "message": extract_data["messageg"]
            }
            
        excel_file = extract_data["excel_file"]
        print(f"Excel File: {excel_file}")
        
        # Open the Excel file in read binary mode
        if not os.path.exists(excel_file):
            return {
                "status": "error",
                "message": "Excel file not found"
            }
            
        headers = {
            "Content-Disposition": f"attachment; filename=output.xlsx"
        }

        # Return FileResponse directly with the file path and headers
        return FileResponse(excel_file, headers=headers, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    except Exception as e:
        return {
            "status": "error",
            "message": e.args
            }
    
if __name__ == '__main__':
    # Start a uvicorn server
    uvicorn.run(app, host="localhost", port=8000)