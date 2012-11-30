from .utils.app import AppSettings

class Settings(AppSettings):
    REALIP = False
    XACCEL = False


app_settings = Settings('FNPDJANGO')
