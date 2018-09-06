import os
import logging


def get_enviroment_value(key):
    try:
        value = os.environ[key]
    except KeyError:
        logging.error("Following key is not set: %s", str(key))
        value = None
    return value


class Config:
    def get_property(self, property_name):
        return get_enviroment_value(property_name)
