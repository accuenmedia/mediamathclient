from mediamathclient.base import Base


class Advertiser(Base):

    def __init__(self, api_key, username, password, data=None):
        super().__init__(api_key, username, password, data)

    def get_all(self):
        url = self.generate_url("advertisers")
        return self.call_mm_api('GET', url)
