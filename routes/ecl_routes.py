from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from utils.auth_utils import get_current_user, check_access
from utils.plotting_utils import plot_ecl_curve
import pandas as pd
import os

router = APIRouter(prefix="/ecl", tags=["ECL"])

DATA_PATH = "app/data/ecl_segment_data.csv"
STATIC_DIR = "app/static"

@router.get("/data/{segment}")
def get_ecl_data(segment: str, user: dict = Depends(get_current_user)):
    check_access(user, ["analyst", "cro"])
    df = pd.read_csv(DATA_PATH)

    if user["role"] == "analyst":
        allowed_segments = ["EDUCATION", "HOMEIMPROVEMENT"]
        if segment.upper() not in allowed_segments:
            raise HTTPException(status_code=403, detail="Segment not assigned")

    seg_data = df[df["segment"].str.upper() == segment.upper()]
    if seg_data.empty:
        raise HTTPException(status_code=404, detail="No ECL data found")

    return seg_data.to_dict(orient="records")

@router.get("/plot/{segment}")
def get_ecl_plot(segment: str, user: dict = Depends(get_current_user)):
    check_access(user, ["analyst", "cro"])
    df = pd.read_csv(DATA_PATH)
    file_path = plot_ecl_curve(df, segment, STATIC_DIR)
    return FileResponse(file_path, media_type="image/png")
