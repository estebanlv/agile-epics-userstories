from pydantic import BaseModel, Field

class ExtendRequest(BaseModel):
    description: str = Field(..., description="The description of the user story to extend.")
