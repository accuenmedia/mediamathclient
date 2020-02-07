from mediamathclient.base import Base


class Advertiser(Base):

    def get_all(self):
        """
        These did not impact the return:
        - self.generate_url("advertisers") + "/?agency_id={0}"
        - self.generate_url("advertisers") + "/?owner.agency_id={0}"
        - self.generate_url("advertisers") + "/?permissions.agency_id={0}"
        - self.generate_url("advertisers") + "/?owner.organization_id={0}"

        :return:
        :rtype:
        """
        url = self.generate_url("advertisers") + "/?owner.organization_id={0}&full=*".format(
            self.organization_id
        )
        return self.call_mm_api('GET', url)
