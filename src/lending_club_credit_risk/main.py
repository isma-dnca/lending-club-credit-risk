from __future__ import annotations

import argparse
from pathlib import Path

from lending_club_credit_risk.config import (
    DEFAULT_THRESHOLD,
    OUTPUT_DIR,
    RAW_DATA_FILE,
    DEFAULT_MODEL_PATH,
    DEFAULT_PREPROCESSOR_PATH,
)

from lending_club_credit_risk.inference.predict import predict_from_csv
from lending_club_credit_risk.modeling.evaluate import evaluate_model
from lending_club_credit_risk.modeling.train import train_lightgbm_model
from lending_club_credit_risk.persistence.save_artifacts import (
    save_metrics,
    save_model,
    save_preprocessor,
)
from lending_club_credit_risk.pipeline.train_pipeline import run_training_pipeline


def _add_train_subparser(subparsers):
    train_parser = subparsers.add_parser(
        "train",
        help="Run the end-to-end training workflow.",
    )
    train_parser.add_argument("--raw-data-file", type=Path, default=RAW_DATA_FILE)
    train_parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    train_parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)

def _add_predict_subparser(subparsers):
    predict_parser = subparsers.add_parser(
        "predict",
        help="Run inference on new data using saved artifacts.",
    )
    predict_parser.add_argument("--input-file", type=Path, required=True)
    predict_parser.add_argument("--model-path", type=Path, default=None)
    predict_parser.add_argument("--preprocessor-path", type=Path, default=None)
    predict_parser.add_argument("--output-file", type=Path, default=None)
    predict_parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Lending Club credit-risk workflows."
    )
    subparsers = parser.add_subparsers(dest="command")

    _add_train_subparser(subparsers)
    _add_predict_subparser(subparsers)

    return parser



def _run_train(args) -> int:
    """
    Run the end-to-end training workflow.
    """

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



def _run_predict(args) -> int:
    """
    Run inference on new data using saved artifacts.
    """
    results = predict_from_csv(
        input_file=args.input_file,
        model_path=(
            args.model_path
            if args.model_path is not None
            else DEFAULT_MODEL_PATH
        ),
        preprocessor_path=(
            args.preprocessor_path
            if args.preprocessor_path is not None
            else DEFAULT_PREPROCESSOR_PATH
        ),
        threshold=args.threshold,
    )

    if args.output_file is not None:
        args.output_file.parent.mkdir(parents=True, exist_ok=True)
        results.to_csv(args.output_file, index=False)
        print(f"Predictions saved to: {args.output_file}")
    else:
        print(results.to_string(index=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "train":
        return _run_train(args)

    if args.command == "predict":
        return _run_predict(args)

    parser.print_help()
    return 1