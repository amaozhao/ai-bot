from ...cores.db import session


class BaseService:
    def __init__(self):
        self.session = session()
