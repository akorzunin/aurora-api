import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from internal.api_router import router
from internal.logger import setup_logging, setup_uvicorn_logging
from internal.settings import IGNORE_CORS, LOG_JSON, LOG_LEVEL

setup_logging(
    json_logs=LOG_JSON,
    log_level=LOG_LEVEL,
)
access_logger = structlog.stdlib.get_logger("api.access")
# log = structlog.stdlib.get_logger(__name__)

app = FastAPI()
setup_uvicorn_logging(app, access_logger)

app.include_router(router)

if IGNORE_CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
