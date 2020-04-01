import os


class _Env:
    """Contains all environment variables required to run the Airflow application.

    Some of the environment variables are re-interpreted as non-string type for the convenience of
    using them.
    """

    @property
    def APP_DEFAULT_FOLIUM_SERVER_URL(self) -> str:
        """Default Folium JS and CSS custom host to use."""
        return os.getenv("APP_DEFAULT_FOLIUM_SERVER_URL", "")

    @property
    def APP_DEFAULT_TILESERVER_URL(self) -> str:
        """Default tileserver custom host to use."""
        return os.getenv("APP_DEFAULT_TILESERVER_URL", "")


Env = _Env()
