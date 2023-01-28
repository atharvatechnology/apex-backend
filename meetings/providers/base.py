class BasicProvider:
    def get_meetings(self):
        raise NotImplementedError

    def create_meetings(self, meeting_config):
        raise NotImplementedError

    def update_meetings(self, *args, **kwargs):
        raise NotImplementedError

    def delete_meetings(self, *args, **kwargs):
        raise NotImplementedError
