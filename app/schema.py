from pydantic import BaseModel


# Define input_data schema
class PatientData(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float # blood pressure
    s2: float # serum measurement 1
    s3: float # serum measurement 2
    s4: float # serum measurement 3
    s4: float # serum measurement 4
    s5: float # serum measurement 5
    s6: float # serum measurement 6

    class Config:
        schema_extra = {
            "example": {
                "age": 0.05,
                "sex": 0.05,
                "bmi": 0.06,
                "bp": 0.02,
                "s1": -0.04,
                "s2": -0.04,
                "s3": -0.02,
                "s4": -0.01,
                "s5": 0.01,
                "s6": 0.02
            }
        }
