from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Optional
from datetime import date, datetime
import re

class ApplicationCreate(BaseModel):
    vacancy_id: int = Field(gt=0, description="ID вакансии")
    resume_url: HttpUrl = Field(description="Ссылка на резюме")
    cover_letter: Optional[str] = Field(None, max_length=2000, description="Сопроводительное письмо")
    
    @field_validator('cover_letter')
    @classmethod
    def not_empty_string(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v.strip() == "":
            raise ValueError('Cover letter cannot be empty if provided')
        return v

class ApplicationResponse(BaseModel):
    id: int
    vacancy_id: int
    student_id: int
    status: str
    applied_at: datetime
    resume_url: str
    
    model_config = {
        "from_attributes": True  
    }

class VacancyCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100, description="Название вакансии")
    description: str = Field(min_length=10, max_length=5000, description="Описание")
    type: str = Field(description="Тип: job или internship")
    location: Optional[str] = Field(None, max_length=200)
    is_on_campus: bool = True
    deadline: date
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v not in ['job', 'internship']:
            raise ValueError('type must be "job" or "internship"')
        return v
    
    @field_validator('deadline')
    @classmethod
    def future_deadline(cls, v: date) -> date:
        if v < date.today():
            raise ValueError('deadline cannot be in the past')
        return v

class VacancyResponse(BaseModel):
    id: int
    title: str
    description: str
    type: str
    location: Optional[str]
    is_on_campus: bool
    deadline: date
    status: str
    
    model_config = {
        "from_attributes": True
    }


class StudentProfileUpdate(BaseModel):
    phone: Optional[str] = Field(None, max_length=20)
    faculty: Optional[str] = Field(None, min_length=2, max_length=100)
    course: Optional[int] = Field(None, ge=1, le=6)
    resume_url: Optional[HttpUrl] = None
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v:
            if not re.match(r'^[\+\d\s\-\(\)]{5,20}$', v):
                raise ValueError('Invalid phone format')
        return v
    
class ReviewCreate(BaseModel):
    to_user_id: int = Field(gt=0)
    type: str
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=1000)
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v not in ['student_review', 'employer_review']:
            raise ValueError('type must be "student_review" or "employer_review"')
        return v
