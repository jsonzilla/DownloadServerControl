from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId
from app.models.program_model import ProgramModel
from app.models.examples.version_request_example import example


class VersionRequestModel(BaseModel):
    client_id: str = Field(description="Client ID")
    description: str = Field(description="A short description of the version.")
    program: ProgramModel = Field(description="The program that this version is for.")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": example}
