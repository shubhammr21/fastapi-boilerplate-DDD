from fastapi import FastAPI

from src import presentation
from src.config import settings
from src.infrastructure.application import configure_logger
from src.infrastructure.application import create as application_factory

# Adjust the logging
# -------------------------------
configure_logger()


# Adjust the application
# -------------------------------
app: FastAPI = application_factory(
    debug=settings.debug,
    rest_routers=(
        presentation.products.rest.router,
        presentation.orders.rest.router,
    ),
    startup_tasks=[],
    shutdown_tasks=[],
    startup_processes=[],
)
