from pydantic import BaseModel, Field, field_validator
from typing import List

class SubTask(BaseModel):
    subtask: str = Field(..., description="A subtask required to complete the user story.")

class AcceptanceCriterion(BaseModel):
    criterion: str = Field(..., description="An acceptance criterion for the user story.")

class ExtendedUserStory(BaseModel):
    story: str = Field(..., description="A brief summary of the user story.")
    description: str = Field(..., description="A detailed description of the user story.")
    effort_points: int = Field(..., description="Effort points required to complete the story.")
    subtasks: List[SubTask] = Field(..., description="List of subtasks.")
    acceptance_criteria: List[AcceptanceCriterion] = Field(..., description="List of acceptance criteria.")
    definition_of_done: str = Field(..., description="Definition of done for the user story.")

    @field_validator('effort_points')
    def validate_effort_points(cls, value):
        if not (1 <= value <= 10):
            raise ValueError('effort_points must be between 1 and 10.')
        return value

class ExtendedUserStorySchema(BaseModel):
    extended_user_story: ExtendedUserStory
