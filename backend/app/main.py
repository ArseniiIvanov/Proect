from fastapi import FastAPI
from app.routrs import vacancies, applications

app = FastAPI()

app.include_router(vacancies.router)
app.include_router(applications.router)
