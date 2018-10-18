"""Application setup at runtime."""

from sanic import Sanic
from sanic.exceptions import SanicException, NotFound, InvalidUsage
from sanic.response import json
from aiocache import SimpleMemoryCache
from aiocache.serializers import JsonSerializer

from geoip.config import DevConfig
from geoip.api.ip import blueprint
from geoip.extensions import ip_lookup


def create_app(config=DevConfig):
    """Application factory for geoIP application.

    Configuration of the application can be passed into this function.
    """
    application = Sanic('geoip')
    application.config.from_object(config)
    application.blueprint(blueprint)
    extensions_setup(application)
    register_error_handlers(application)
    return application


def extensions_setup(app):
    """Initialize the extensions of the application."""
    ip_lookup.init_app(app)


def register_error_handlers(app):
    """Register some simple error handlers on the application."""
    @app.exception(NotFound)
    def not_found_handler(request, exception):
        """Handle 404 exceptions."""
        response = dict(
            error='Not Found',
            url=request.url,
            message=','.join(exception.args))
        return json(response, status=404)

    @app.exception(InvalidUsage)
    def invalid_usage_handler(request, exception):
        """Handle InvalidUsage exceptions.

        InvalidUsage is used in this application as to point out bad requests
        """
        response = dict(
            error='Bad request',
            message=','.join(exception.args))
        return json(response, status=400)
