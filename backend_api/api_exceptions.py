class NoSuchData(Exception):
    def __init__(
        self,
        message,
        status_code=None,
        payload=None
    ):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def to_dict(self):
        res = dict(self.payload or ())
        res['message'] = self.message

        return res