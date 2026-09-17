from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator

class OpportunityLevel(str, Enum): HIGH = "HIGH"; MEDIUM = "MEDIUM"; LOW = "LOW"
class AnalyzeTaskRequest(BaseModel):
    task: str = Field(max_length=2000)
    @field_validator("task")
    @classmethod
    def task_must_contain_text(cls, value: str) -> str:
        value = value.strip()
        if not value: raise ValueError("Task cannot be empty.")
        return value
class AIOpportunity(BaseModel): level: OpportunityLevel; message: str
class WorkflowStep(BaseModel): step: int = Field(ge=1); title: str; description: str
class SkillToPractice(BaseModel): name: str; category: str; level: str
class AnalysisResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    task: str
    ai_opportunity: AIOpportunity = Field(alias="aiOpportunity")
    recommended_workflow: list[WorkflowStep] = Field(alias="recommendedWorkflow")
    skill_to_practice: SkillToPractice = Field(alias="skillToPractice")
    ready_to_use_prompt: str = Field(alias="readyToUsePrompt")
    expected_benefit: str = Field(alias="expectedBenefit")
    human_review: str = Field(alias="humanReview")
class FeedbackRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    task: str = Field(min_length=1, max_length=2000)
    usefulness: str = Field(min_length=1, max_length=40)
    time_saved: str = Field(alias="timeSaved", min_length=1, max_length=40)
    improvement: str = Field(default="", max_length=1000)
    @field_validator("task", "usefulness", "time_saved")
    @classmethod
    def required_text_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value: raise ValueError("This field cannot be empty.")
        return value
class FeedbackResponse(BaseModel): success: bool; message: str
