from pydantic import BaseModel, Field, field_validator
from typing import List

class UserStory(BaseModel):
    story: str = Field(..., description="A brief summary of the user story.")
    description: str = Field(..., description="A detailed description of the user story.")
    effort_points: int = Field(..., description="Effort points required to complete the story.")

    @field_validator('effort_points')
    def validate_effort_points(cls, value):
        if not (1 <= value <= 13):
            raise ValueError('effort_points must be between 1 and 13.')
        return value

class UserStorySchema(BaseModel):
    user_stories: List[UserStory]
