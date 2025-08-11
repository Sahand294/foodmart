from models import SiteSetting
class Connect:
    @staticmethod
    def get_value(key):
        value = SiteSetting.query.filter_by(key=key).first()
        if value:
            return value.Value
        return None