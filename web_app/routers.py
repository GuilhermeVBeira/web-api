import logging
from importlib import import_module

logger = logging.getLogger(__name__)

app_routers = [
    "web_app.apps.auth.routers",
    "web_app.apps.users.routers",
    "web_app.apps.clients.routers",
]


def load_routers(app):
    for path in app_routers:
        module = import_module(path)

        function = getattr(module, "include_router")
        function(app)

        logger.info("Initialized router to %s", path)
