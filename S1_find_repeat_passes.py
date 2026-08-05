# ---- This is <S1_find_repeat_passes.py> ----

"""
Find repeat passes for S1 input image.

Requirements: https://github.com/jlo031/CDSE
(NB: Updated version after 2036-03-13)
"""

import pathlib
import sys

from loguru import logger

import CDSE.utils as CDSE_utils
import CDSE.json_utils as CDSE_json
import CDSE.search_and_download as CDSE_sd

from config.load_config import *

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

loglevel = "DEBUG"

# Provide S1 image name       
S1_name = "S1A_EW_GRDM_1SDH_20251028T122115_20251028T122215_061625_07B2D6_AC47"

# Provide center lat/lon
lat = -63.25
lon = 111.0

# Provide timing
start_date   = '2022-08-01'
end_date     = '2022-10-31'
start_time   = '00:00:01'
end_time     = '23:59:59'

# Set standard earch parameters
sensor       = 'Sentinel-1'
product_type = 'GRD'

# Download products
download = True

# Read CDSE user credentials from '.env'
username, password = CDSE_utils.get_user_and_passwd()

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

# Find S1 product and get relative orbit
S1_d = CDSE_sd.search_CDSE_catalogue_by_name(S1_name)
S1_p = S1_d["value"]

if len(S1_p) != 1:
    logger.error("Found more than one product.")

for attribute in S1_p[0]['Attributes']:
    if attribute["Name"] == "relativeOrbitNumber":
        relative_orbit = attribute["Value"]

logger.info(f"relative orbit: {relative_orbit}")

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

# Build location dict
pos_D = dict()
pos_D['lat'] = lat
pos_D['lon'] = lon

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
    relative_orbit = relative_orbit,
    max_results = 1000,
    expand_attributes = True,
    loglevel = loglevel,
)

product_list = response_json['value']

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

p_names = []
for p in product_list:
    p_names.append(f"{p['Name']}")
p_names.sort()


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

# ---- End of <S1_find_repeat_passes.py> ----

