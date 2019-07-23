from mediamathclient.base import Base


class Advertiser(Base):

    def get_all(self):
        url = self.generate_url("advertisers")
        return self.call_mm_api('GET', url)
