# ---- This is <S1_query_and_download.py> ----

"""
Query CDSE for Sentinel-1 products for the MIZ voyage.
Search location is currently centered on "Center Buoy" from Klaus' coordinate file.
Download products according to defined specifications.
"""

import pathlib
import sys

from loguru import logger

from shapely import wkt
from shapely.geometry import shape

import numpy as np

import CDSE.utils as CDSE_utils
import CDSE.json_utils as CDSE_json
import CDSE.search_and_download as CDSE_sd

from config.load_config import *

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

# Set loglevel
loglevel = "DEBUG"

logger.remove()
logger.add(sink=sys.stdout, level=loglevel)

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

logger.debug(f"DATA_DIR:    {DATA_DIR}")
logger.debug(f"S1_DIR:      {S1_DIR}")
logger.debug(f"S1_L1_DIR:   {S1_L1_DIR}")
logger.debug(f"S1_FEAT_DIR: {S1_FEAT_DIR}")
logger.debug(f"S1_GEO_DIR:  {S1_GEO_DIR}")

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

# Set search parameters
sensor       = 'Sentinel-1'
start_date   = '2025-08-01'
end_date     = '2025-10-31'
product_type = 'GRD'
start_time   = '00:00:01'
end_time     = '23:59:59'

# Read CDSE user credentials from '.env'
username, password = CDSE_utils.get_user_and_passwd()

# Define ROI lat/lon
lat = -63.25
lon = 111.0
pos_D = dict()
pos_D['lat'] = lat
pos_D['lon'] = lon

# Specify download
download = True

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

# Search for products

response_json = CDSE_sd.search_CDSE_catalogue(
    sensor,
    pos_D,
    start_date,
    end_date,
    start_time = start_time,
    end_time = end_time,
    sensor_mode = None,
    product_type = product_type,
    processing_level = None,
    max_results = 1000,
    expand_attributes = True,
    loglevel = loglevel,
)

product_list = response_json['value']

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

# Download products

if download:

    logger.info("Downloading all EW products (non-COG, dual-pol)")

    download_minimum_overlap = False

    # loop over products and get overlaps
    for p in product_list:
    
        logger.debug(f"{p['Name']}")

        if not 'COG' in p['Name'] and '1SDH' in p['Name'] and 'EW' in p['Name']:
            logger.info(f"{p['Name']}")
            logger.info("    Downloading this product")
        
            CDSE_sd.download_product_from_cdse(p, S1_L1_DIR, username, password)

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

# ---- End of <S1_query_and_download.py> ----
