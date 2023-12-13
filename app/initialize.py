""" Init project """

from functools import lru_cache

##########################################
# Initialize configuration for EDR pages #
##########################################

@lru_cache()
def get_base_url() -> str:
    """
    Parse configuration file and return base_url
    """
    return "http://localhost:5000/"


@lru_cache
def get_data_path() -> str:
    """
    Returns config parameter object
    """
    return "data"


@lru_cache
def get_filename() -> str:
    """
    Returns config parameter object
    """
    return "data/T_YTNE85_C_ENMI_20231213000000.bin"


# @lru_cache
# def get_config_collections():
#     """
#     Returns config collections object
#     """
#     return get_edr_config('collections')
