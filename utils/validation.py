from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str = Field(..., min_length=1)
    education: Optional[str] = ""
    experience: Optional[str] = ""
    skills: List[str] = Field(..., min_length=1)
    interests: List[str] = []
    learning_style: Optional[str] = ""

    @field_validator("name")
    @classmethod
    def name_required(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Name is required")
        return cleaned

    @field_validator("education", "experience", "learning_style", mode="before")
    @classmethod
    def strip_optional_text(cls, value):
        if value is None:
            return ""
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("skills", "interests", mode="before")
    @classmethod
    def normalize_list_fields(cls, value):
        if value is None:
            return []
        if isinstance(value, str):
            items = [item.strip() for item in value.split(",")]
            return [item for item in items if item]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        return value

    @field_validator("skills")
    @classmethod
    def skills_required(cls, value: List[str]) -> List[str]:
        if not value:
            raise ValueError("At least one skill is required")
        return value


__all__ = ["AnalyzeRequest", "ValidationError"]
