from __future__ import annotations

import argparse
from pathlib import Path

from lending_club_credit_risk.config import (
    DEFAULT_THRESHOLD,
    OUTPUT_DIR,
    RAW_DATA_FILE,
)
from lending_club_credit_risk.modeling.evaluate import evaluate_model
from lending_club_credit_risk.modeling.train import train_lightgbm_model
from lending_club_credit_risk.persistence.save_artifacts import (
    save_metrics,
    save_model,
    save_preprocessor,
)
from lending_club_credit_risk.pipeline.train_pipeline import run_training_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Train the Lending Club credit-risk pipeline end to end."
    )
    parser.add_argument("--raw-data-file", type=Path, default=RAW_DATA_FILE)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    return parser


def main(argv: list[str] | None = None) -> int:
    """
    Run the end-to-end training workflow.
    """
    args = build_parser().parse_args(argv)

    model_path = args.output_dir / "models" / "lightgbm_model.joblib"
    preprocessor_path = args.output_dir / "preprocessors" / "preprocessor.joblib"
    metrics_path = args.output_dir / "reports" / "metrics.json"

    (
        X_train_processed,
        X_test_processed,
        y_train,
        y_test,
        preprocessor,
    ) = run_training_pipeline(raw_data_file=args.raw_data_file)

    model = train_lightgbm_model(X_train_processed, y_train)
    metrics = evaluate_model(
        model,
        X_test_processed,
        y_test,
        threshold=args.threshold,
    )

    save_model(model, model_path)
    save_preprocessor(preprocessor, preprocessor_path)
    save_metrics(metrics, metrics_path)

    print("Training pipeline executed successfully.")
    print(f"Model saved to: {model_path}")
    print(f"Preprocessor saved to: {preprocessor_path}")
    print(f"Metrics saved to: {metrics_path}")
    print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")

    return 0