from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl
from bson import ObjectId
from app.codecs import ObjectIdCodec
from app.models.program_model import ProgramModel
from app.models.examples.version_example import example


class VersionModel(BaseModel):
    id: ObjectIdCodec = Field(default_factory=ObjectIdCodec, alias="_id")
    description: str = Field(description="A short description of the version.")
    link: HttpUrl = Field(description="The link to the version.")
    start_date_time: Optional[datetime] = Field(default_factory=datetime.utcnow, description="The date and time that this version starts.")
    end_date_time: Optional[datetime] = Field(description="The date and time that this version ends.")
    program: ProgramModel = Field(description="The program that this version is for.")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": example}


class UpdateVersionModel(BaseModel):
    description: Optional[str] = Field(description="A short description of the version.")
    link: Optional[HttpUrl] = Field(description="The link to the version.")
    start_date_time: Optional[datetime] = Field(default_factory=datetime.utcnow, description="The date and time that this version starts.")
    end_date_time: Optional[datetime] = Field(description="The date and time that this version ends.")
    program: Optional[ProgramModel] = Field(description="The program that this version is for.")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": example}
