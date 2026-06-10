FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./

COPY src/ src/

RUN python -m pip install .

COPY outputs/models outputs/models/

COPY outputs/preprocessors outputs/preprocessors/

EXPOSE 8000

CMD ["uvicorn", "lending_club_credit_risk.api.app:app", "--host", "0.0.0.0", "--port", "8000"]

