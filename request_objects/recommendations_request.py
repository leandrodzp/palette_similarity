from pydantic import BaseModel

class RecommendationsRequest(BaseModel):
    palette: list
    filters : dict

