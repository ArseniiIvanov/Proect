from typing import Optional, List
from datetime import datetime, date
from sqlalchemy import String, Boolean, Text, Date, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    student: Mapped[Optional["Student"]] = relationship("Student", back_populates="user", uselist=False)
    employer: Mapped[Optional["Employer"]] = relationship("Employer", back_populates="user", uselist=False)
    reviews_from: Mapped[List["Review"]] = relationship("Review", foreign_keys="Review.from_user_id", back_populates="from_user")
    reviews_to: Mapped[List["Review"]] = relationship("Review", foreign_keys="Review.to_user_id", back_populates="to_user")
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="user")

class Student(Base):
    __tablename__ = "students"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    faculty: Mapped[str] = mapped_column(String(100), nullable=False)
    course: Mapped[Optional[int]] = mapped_column(Integer)
    resume_url: Mapped[Optional[str]] = mapped_column(String(255))

    user: Mapped["User"] = relationship("User", back_populates="student")
    applications: Mapped[List["Application"]] = relationship("Application", back_populates="student")
    interviews: Mapped[List["Interview"]] = relationship("Interview", back_populates="student")
    subscriptions: Mapped[List["Subscription"]] = relationship("Subscription", back_populates="student")

class Employer(Base):
    __tablename__ = "employers"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(20))
    department: Mapped[Optional[str]] = mapped_column(String(100))

    user: Mapped["User"] = relationship("User", back_populates="employer")
    vacancies: Mapped[List["Vacancy"]] = relationship("Vacancy", back_populates="employer")

class Vacancy(Base):
    __tablename__ = "vacancies"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(200))
    is_on_campus: Mapped[bool] = mapped_column(Boolean, default=True)
    employer_id: Mapped[int] = mapped_column(ForeignKey("employers.id"))
    deadline: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    employer: Mapped["Employer"] = relationship("Employer", back_populates="vacancies")
    applications: Mapped[List["Application"]] = relationship("Application", back_populates="vacancy")
    interviews: Mapped[List["Interview"]] = relationship("Interview", back_populates="vacancy")
    skills: Mapped[List["Skill"]] = relationship("Skill", secondary="vacancy_skills", back_populates="vacancies")

class Application(Base):
    __tablename__ = "applications"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    resume_url: Mapped[str] = mapped_column(String(255), nullable=False)
    cover_letter: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    applied_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    vacancy: Mapped["Vacancy"] = relationship("Vacancy", back_populates="applications")
    student: Mapped["Student"] = relationship("Student", back_populates="applications")

class Review(Base):
    __tablename__ = "reviews"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    from_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[Optional[str]] = mapped_column(String(20))
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    from_user: Mapped["User"] = relationship("User", foreign_keys=[from_user_id], back_populates="reviews_from")
    to_user: Mapped["User"] = relationship("User", foreign_keys=[to_user_id], back_populates="reviews_to")

class Interview(Base):
    __tablename__ = "interviews"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"))
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    meeting_link: Mapped[Optional[str]] = mapped_column(String(255))
    reminder_sent: Mapped[bool] = mapped_column(Boolean, default=False)

    student: Mapped["Student"] = relationship("Student", back_populates="interviews")
    vacancy: Mapped["Vacancy"] = relationship("Vacancy", back_populates="interviews")

class Notification(Base):
    __tablename__ = "notifications"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[Optional[str]] = mapped_column(String(200))
    message: Mapped[Optional[str]] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    user: Mapped["User"] = relationship("User", back_populates="notifications")

class Skill(Base):
    __tablename__ = "skills"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    vacancies: Mapped[List["Vacancy"]] = relationship("Vacancy", secondary="vacancy_skills", back_populates="skills")

class VacancySkill(Base):
    __tablename__ = "vacancy_skills"
    
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), primary_key=True)

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    vacancy_type: Mapped[Optional[str]] = mapped_column(String(20))
    faculty_filter: Mapped[Optional[str]] = mapped_column(String(100))

    student: Mapped["Student"] = relationship("Student", back_populates="subscriptions")