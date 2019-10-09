class Empty:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def on_get(self, req, resp):
        pass
    def on_post(self, req, resp):
        pass