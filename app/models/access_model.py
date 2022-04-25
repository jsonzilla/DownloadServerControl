from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId
from app.codecs.object_id_codec import ObjectIdCodec
from app.codecs.datetime_codec import DatetimeCodec
from app.models.program_model import ProgramModel
from app.models.examples.access_example import example


class AccessModel(BaseModel):
    id: ObjectIdCodec = Field(default_factory=ObjectIdCodec, alias="_id")
    client_id: str = Field(alias="client_id")
    date_time: datetime = Field(default_factory=DatetimeCodec, description="The date and time that this access was made.")
    program_request: ProgramModel = Field(description="The program that this version that user is requesting access to.")
    program_response: ProgramModel = Field(description="The program that this version that user received access to.")
    client_host: str = Field(description="The hostname of the client that requested access.")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": example}
