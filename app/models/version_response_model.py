from pydantic import AnyUrl, BaseModel, Field


class VersionResponseModel(BaseModel):
    url: AnyUrl = Field(description="The URL of the version.")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
