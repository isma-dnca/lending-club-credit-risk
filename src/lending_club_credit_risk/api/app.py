from fastapi import FastAPI

from lending_club_credit_risk.api.schemas import HealthResponse


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI app.
    """
    app = FastAPI(
        title="Lending Club Credit Risk API",
    )

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        """
        Health check endpoint to verify that the API is running.
        """
        return HealthResponse(status="ok")
    return app


app = create_app()