from pydantic import BaseModel

from fastapi import FastAPI, File, UploadFile

class GeneratePaletteRequest(BaseModel):
    file: UploadFile = File(...)
