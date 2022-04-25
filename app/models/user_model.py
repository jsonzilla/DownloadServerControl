from typing import Optional
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, SecretStr, validator
from app.codecs import DatetimeCodec, ObjectIdCodec
from app.models.examples.user_example import example


class UserModel(BaseModel):
    id: ObjectIdCodec = Field(default_factory=ObjectIdCodec, alias="_id")
    username: str = Field(unique_items=None, min_length=3, max_length=50, description="The username of the user.")
    password: SecretStr = Field(description="The password of the user.")
    email: EmailStr = Field(unique_items=None, description="The email of the user.")
    last_update_datetime: datetime = Field(default_factory=DatetimeCodec, description="The date and time that this user was last updated.")

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": example}


class ShowUserModel(BaseModel):
    id: ObjectIdCodec = Field(default_factory=ObjectIdCodec, alias="_id")
    username: str = Field(unique_items=None, min_length=3, max_length=50)
    email: EmailStr = Field(unique_items=None, description="The email of the user.")
    last_update_datetime: datetime = Field(default_factory=DatetimeCodec, description="The date and time that this user was last updated.")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": example}


class UpdateUserModel(BaseModel):
    username: Optional[str] = Field(unique_items=None, min_length=3, max_length=50)
    password: Optional[str] = Field(description="The password of the user.")
    email: EmailStr = Field(unique_items=None, description="The email of the user.")
    last_update_datetime: Optional[datetime] = Field(description="The date and time that this user was last updated.")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": example}
