import threading
import logging
from src.model.orm_model import OrmModel


class OrmView(object):

    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(OrmView, "_instance"):
            with OrmView._instance_lock:
                if not hasattr(OrmView, "_instance"):
                    OrmView._instance = \
                        super(OrmView, cls).__new__(cls, *args, **kwargs)
        return OrmView._instance

    def query_data_view(self, input_params):
        orm_model = OrmModel()
        query_result = orm_model.query_data_model(input_params)
        logging.info(query_result)
        return input_params
