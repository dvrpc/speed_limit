import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine

load_dotenv(find_dotenv())

ANALYSIS_URL = os.getenv("analysis_url")
GIS_URL = os.getenv("gis_url")
ENGINE = create_engine(ANALYSIS_URL)
GIS_ENGINE = create_engine(GIS_URL)
DATA_ROOT = os.getenv("data_root")