from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str


class PredictionRequest(BaseModel):
    id: int | None = None
    title: str
    desc: str
    zip_code: str
    issue_d: str
    emp_length: str
    loan_amnt: float
    revenue: float
    fico_n: float
    purpose: str
    addr_state: str
    home_ownership_n: int
    dti_n: float
    experience_c: int


class PredictionResponse(BaseModel):
    id: int | None = None
    default_probability: float
    predicted_default: int
    