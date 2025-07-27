from models.sitesetting import SiteSetting
class Connect:
    @staticmethod
    def get_value(key):
        value = SiteSetting.query.filter_by(key=str(key)).first()
        if value:
            return value.Value
        return None