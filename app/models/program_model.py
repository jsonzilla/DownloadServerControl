from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from app.codecs import ObjectIdCodec


class ProgramModel(BaseModel):
    id: ObjectIdCodec = Field(default_factory=ObjectIdCodec, alias="_id")
    application_name: str = Field(description="The general application name in lowercase, e.g. 'visu'")
    release: int = Field(gt=2010, le=2199, description="The release number of the application, e.g. '2021'")
    revision: int = Field(gt=201001, le=219901, description="The revision number of this program in numeric format.")
    protection: str = Field(description="The protection type of this program.")
    language: str = Field(regex="^[a-z]{2}-[A-Z]{2}$", description="Language code, e.g. 'en-EN'")
    subscription: str = Field(description="Subscription type, e.g. 'subscription'")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateBlock(BaseModel):
    application_name: Optional[str] = Field(description="The general application name in lowercase, e.g. 'visu'")
    release: Optional[int] = Field(gt=2010, le=2199, description="The release number of the application, e.g. '2021'")
    revision: Optional[int] = Field(gt=201001, le=219901, description="The revision number of this program in numeric format.")
    protection: Optional[str] = Field(description="The protection type of this program.")
    language: Optional[str] = Field(regex="^[a-z]{2}-[A-Z]{2}$", description="Language code, e.g. 'en-EN'")
    subscription: Optional[str] = Field(description="Subscription type, e.g. 'subscription'")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
