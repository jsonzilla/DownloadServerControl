from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId
from app.codecs import ObjectIdCodec
from app.models.program_model import ProgramModel
from app.models.examples.block_example import example


class BlockModel(BaseModel):
    id: ObjectIdCodec = Field(default_factory=ObjectIdCodec, alias="_id")
    description: str = Field(description="A short description of the blocked version.")
    start_date_time: Optional[datetime] = Field(default_factory=datetime.utcnow, description="The date and time that this block starts.")
    end_date_time: Optional[datetime] = Field(description="The date and time that this block ends.")
    program: ProgramModel = Field(description="The program that will be blocked.")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": example}


class UpdateBlockModel(BaseModel):
    description: Optional[str] = Field(description="A short description of the blocked version.")
    start_date_time: Optional[datetime] = Field(default_factory=datetime.utcnow, description="The date and time that this block starts.")
    end_date_time: Optional[datetime] = Field(description="The date and time that this block ends.")
    program: Optional[ProgramModel] = Field(description="The program that will be blocked.")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": example}
