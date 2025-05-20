from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.image_processor import ImageProcessor
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ColorSuggestion(BaseModel):
    colors: List[str]

class SkinToneChange(BaseModel):
    l: float
    a: float
    b: float

@router.post("/analyze", response_model=ColorSuggestion)
async def analyze_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        lab_values = ImageProcessor.extract_skin_tone(contents)
        suggested_colors = ImageProcessor.suggest_colors(lab_values)
        return ColorSuggestion(colors=suggested_colors)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/change-skin-tone")
async def change_skin_tone(file: UploadFile = File(...), target_lab: SkinToneChange):
    try:
        contents = await file.read()
        new_image_bytes = ImageProcessor.change_skin_tone(contents, (target_lab.l, target_lab.a, target_lab.b))
        return Response(content=new_image_bytes, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))