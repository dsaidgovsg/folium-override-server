import os
from typing import List, Optional


class _Env:
    """Contains all environment variables required to run the Airflow application.

    Some of the environment variables are re-interpreted as non-string type for the convenience of
    using them.
    """

    @property
    def APP_DEFAULT_FOLIUM_SERVER_URL(self) -> Optional[str]:
        """Default Folium JS and CSS custom host to use."""
        return os.getenv("APP_DEFAULT_FOLIUM_SERVER_URL")

    @property
    def APP_DEFAULT_TILESERVER_GL_URL(self) -> Optional[str]:
        """Default tileserver-gl custom host to use."""
        return os.getenv("APP_DEFAULT_TILESERVER_GL_URL")

    @property
    def APP_TILESERVER_GL_TILES(self) -> List[str]:
        """
        Available tileserver-gl tiles to use. Multiple identifiers are delimited by comma.

        The tile set must be present in the custom tileserver-gl.
        """
        return os.getenv("APP_TILESERVER_GL_TILES", "osm_bright,dark_matter").split(",")


Env = _Env()
