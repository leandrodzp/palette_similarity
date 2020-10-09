from fastapi import FastAPI, File, UploadFile
import uvicorn

from palette_generator import paletteFromImage
from constants import AMOUNT_OF_COLORS
from palette_embedding.palette_embedding import PaletteEmbeddingModel

app = FastAPI()

@app.post("/generate_palette/")
async def generate_palette(file: UploadFile = File(...)):
    response = {
        "number_of_colors" : AMOUNT_OF_COLORS,
        "palette" : paletteFromImage(file)
    }
    return response

@app.post("/recommendations/")
async def generate_palette(query_params: RecommendationsRequest):
    
    algorithm_entry = '-'.join(query_params.palette)
    model = PaletteEmbeddingModel()
    embedding = model.Embed(palette=algorithm_entry)

    # Here we should call the elastic searcher with query_params.filters
    response = {
        "recommendations": "This should be the response from Elastic",
        }

    return response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
