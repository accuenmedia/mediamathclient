from mediamathclient.base import Base


class Advertiser(Base):

    def get_all(self):
        url = self.generate_url("advertisers") + "/?owner.organization_id={0}&full=*".format(
            self.organization_id
        )
        return self.call_mm_api('GET', url)
