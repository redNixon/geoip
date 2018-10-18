"""Extensions for the geoIP application.

Extensions allow for configuration at runtime using a bare,
non-configured class initialized at import, and calling
'init_app' at runtime to configure the application
extension with app-specific configuration.

See geoip.config for configuration.
"""

from geoip.utils import GeoIP

ip_lookup = GeoIP()
