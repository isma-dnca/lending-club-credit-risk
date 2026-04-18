from src.config import PROJECT_ROOT
from src.modeling.evaluate import evaluate_model
from src.modeling.train import train_lightgbm_model
from src.persistence.save_artifacts import (
    save_metrics,
    save_model,
    save_preprocessor,
)
from src.pipeline.train_pipeline import run_training_pipeline


MODEL_OUTPUT_PATH = PROJECT_ROOT / "outputs" / "models" / "lightgbm_model.joblib"
PREPROCESSOR_OUTPUT_PATH = (
    PROJECT_ROOT / "outputs" / "preprocessors" / "preprocessor.joblib"
)
METRICS_OUTPUT_PATH = PROJECT_ROOT / "outputs" / "reports" / "metrics.json"
THRESHOLD = 0.5


def main() -> None:
    """
    Run the end-to-end training workflow.

    Steps
    -----
    1. Run the preprocessing pipeline
    2. Train the LightGBM model
    3. Evaluate the trained model
    4. Save artifacts and metrics
    """
    (
        X_train_processed,
        X_test_processed,
        y_train,
        y_test,
        preprocessor,
    ) = run_training_pipeline()

    model = train_lightgbm_model(X_train_processed, y_train)
    metrics = evaluate_model(model, X_test_processed, y_test, threshold=THRESHOLD)

    save_model(model, MODEL_OUTPUT_PATH)
    save_preprocessor(preprocessor, PREPROCESSOR_OUTPUT_PATH)
    save_metrics(metrics, METRICS_OUTPUT_PATH)

    print("Training pipeline executed successfully.")
    print(f"Model saved to: {MODEL_OUTPUT_PATH}")
    print(f"Preprocessor saved to: {PREPROCESSOR_OUTPUT_PATH}")
    print(f"Metrics saved to: {METRICS_OUTPUT_PATH}")
    print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")


if __name__ == "__main__":
    main()
