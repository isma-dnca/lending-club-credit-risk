import pytest
import joblib
import pandas as pd

from lending_club_credit_risk.main import build_parser, main
from lending_club_credit_risk.modeling.train import train_lightgbm_model
from lending_club_credit_risk.pipeline.train_pipeline import run_training_pipeline
from tests.test_inference import _write_inference_dataset, _write_training_dataset



def test_build_parser_recognizes_train_command():
    parser = build_parser()
    args = parser.parse_args(["train"])
    assert args.command == "train"



def test_build_parser_recognizes_predict_command():
    parser = build_parser()
    args = parser.parse_args(["predict", "--input-file", "data.csv"])
    assert args.command == "predict"



def test_build_parser_predict_command_requires_input_file():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["predict"])



def test_main_predict_writes_output_file(tmp_path):
    train_file = _write_training_dataset(tmp_path / "train.csv")

    X_train_processed, _, y_train, _, preprocessor = run_training_pipeline(
        raw_data_file=train_file,
        test_size=0.2,
        target_column="default",
    )
    model = train_lightgbm_model(X_train_processed, y_train)

    model_path = tmp_path / "model.joblib"
    preprocessor_path = tmp_path / "preprocessor.joblib"
    output_file = tmp_path / "predictions.csv"

    joblib.dump(model, model_path)
    joblib.dump(preprocessor, preprocessor_path)

    inference_file = _write_inference_dataset(tmp_path / "inference.csv")

    exit_code = main(
        [
            "predict",
            "--input-file",
            str(inference_file),
            "--model-path",
            str(model_path),
            "--preprocessor-path",
            str(preprocessor_path),
            "--output-file",
            str(output_file),
            "--threshold",
            "0.5",
        ]
    )

    assert exit_code == 0
    assert output_file.exists()

    results = pd.read_csv(output_file)

    assert list(results.columns) == [
        "id",
        "default_probability",
        "predicted_default",
    ]
    assert len(results) == 2
    assert results["id"].tolist() == [101, 102]
