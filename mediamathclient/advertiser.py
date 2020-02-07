from mediamathclient.base import Base


class Advertiser(Base):

    def get_all(self, organization_id):
        url = self.generate_url("advertisers", {"agency.organization": organization_id})
        return self.call_mm_api('GET', url)
