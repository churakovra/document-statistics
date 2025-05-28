from app.config.version import __version__

class AppService:
    @staticmethod
    def check_status():
        pass

    @staticmethod
    def get_version() -> str:
        version = __version__
        return version