from fastapi import FastAPI
from pydantic import BaseModel

from .crud import add_lawyer, get_all_lawyers

app = FastAPI()

class Lawyer(BaseModel):

    full_name: str

    email: str

    mobile_number: str

    office_address: str

    bar_council_enrolment_number: str

    state_bar_council: str

    years_of_experience: int

    primary_practice_area: str

@app.post("/lawyers/register")

def register_lawyer(lawyer: Lawyer):

    add_lawyer(

        lawyer.full_name,

        lawyer.email,

        lawyer.mobile_number,

        lawyer.office_address,

        lawyer.bar_council_enrolment_number,

        lawyer.state_bar_council,

        lawyer.years_of_experience,

        lawyer.primary_practice_area,

        "",

        ""

    )

    return {

        "message": "Lawyer registered successfully."

    }

@app.get("/lawyers")

def get_lawyers():

    lawyers = get_all_lawyers()

    return [

        dict(lawyer)

        for lawyer in lawyers

    ]

