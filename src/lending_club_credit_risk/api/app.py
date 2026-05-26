import pandas as pd
<<<<<<< HEAD
from pathlib import Path
=======
>>>>>>> cb9dce4f3841131a22c9170f178fec79eef78c82
from fastapi import FastAPI

from lending_club_credit_risk.api.schemas import (
    HealthResponse,
    PredictionResponse,
    PredictionRequest,
)
from lending_club_credit_risk.inference.predict import predict_from_dataframe
<<<<<<< HEAD
from lending_club_credit_risk.config import DEFAULT_MODEL_PATH, DEFAULT_PREPROCESSOR_PATH
=======
>>>>>>> cb9dce4f3841131a22c9170f178fec79eef78c82


def create_app(
    model_path: str | Path = DEFAULT_MODEL_PATH,
    preprocessor_path: str | Path = DEFAULT_PREPROCESSOR_PATH,
) -> FastAPI:
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



    @app.post("/predict", response_model=PredictionResponse)
    def predict(request: PredictionRequest) -> PredictionResponse:
        """
        Run inference on a single data point provided in the request body and return the prediction results.
        """
        request_data = request.model_dump()
        df = pd.DataFrame([request_data])
<<<<<<< HEAD
        results = predict_from_dataframe(model_path=model_path, preprocessor_path=preprocessor_path, df=df)
=======
        results = predict_from_dataframe(df=df)
>>>>>>> cb9dce4f3841131a22c9170f178fec79eef78c82
        result_row = results.iloc[0]

        return PredictionResponse(
            id=result_row["id"] if "id" in result_row else None,
            default_probability=result_row["default_probability"],
            predicted_default=result_row["predicted_default"],
        )


    return app


app = create_app()