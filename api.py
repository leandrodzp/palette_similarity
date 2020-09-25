from fastapi import FastAPI, File, UploadFile
import uvicorn

from palette_generator import paletteFromImage
from constants import AMOUNT_OF_COLORS

app = FastAPI()

@app.post("/generate_palette/")
async def generate_palette(file: UploadFile = File(...)):
    response = {
        "number_of_colors" : AMOUNT_OF_COLORS,
        "palette" : paletteFromImage(file)
    }
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port="8000")
