import threading
import logging
from src.view.orm_view import OrmView


class OrmController(object):

    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(OrmController, "_instance"):
            with OrmController._instance_lock:
                if not hasattr(OrmController, "_instance"):
                    OrmController._instance = \
                        super(OrmController, cls).__new__(cls, *args, **kwargs)
        return OrmController._instance

    def query_data_controller(self, input_params):
        orm_view = OrmView()
        logging.info(input_params)
        return orm_view.query_data_view(input_params)
