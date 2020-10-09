from fastapi import FastAPI, File, UploadFile
import uvicorn

from palette_generator import paletteFromImage
from constants import AMOUNT_OF_COLORS

# Defines request objects to clean the API
from request_objects.generate_palette_request import GeneratePaletteRequest
from request_objects.recommendations_request import RecommendationsRequest

app = FastAPI()

@app.post("/generate_palette/")
async def generate_palette(query_params: GeneratePaletteRequest):
    response = {
        "number_of_colors" : AMOUNT_OF_COLORS,
        "palette" : paletteFromImage(query_params.file)
    }
    return response

@app.post("/recommendations/")
async def generate_palette(query_params: RecommendationsRequest):
    embedded_palette = query_params.palette
    response = { "recommendations": "This should be the response from Elastic" }
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
