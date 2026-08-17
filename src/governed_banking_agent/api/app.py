from fastapi import FastAPI

from governed_banking_agent import __version__
from governed_banking_agent.api.routes import router


def create_app() -> FastAPI:
    application = FastAPI(
        title="Governed Banking Agent",
        version=__version__,
        description="Validation-first API for a synthetic banking policy research agent.",
    )
    application.include_router(router)
    return application


app = create_app()

