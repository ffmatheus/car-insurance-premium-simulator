from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.config.settings import settings


def create_application() -> FastAPI:
    application = FastAPI(
        title="Car Insurance Premium Simulator",
        description="A FastAPI service for calculating car insurance premiums based on a car's age, value, and other factors.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        debug=settings.DEBUG,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/health", tags=["HEALTH"])
    async def health_check():
        return {"status": "healthy"}

    @application.get("/teste", tags=["TESTE"])
    async def health_check():
        return {"teste": "funcionando"}

    def custom_openapi():
        if application.openapi_schema:
            return application.openapi_schema

        openapi_schema = get_openapi(
            title="Car Insurance Premium Simulator API",
            version="1.0.0",
            description="A FastAPI service for calculating car insurance premiums based on a car's age, value, and other factors.",
            routes=application.routes,
        )

        application.openapi_schema = openapi_schema
        return application.openapi_schema

    application.openapi = custom_openapi

    return application


app = create_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.presentation.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
