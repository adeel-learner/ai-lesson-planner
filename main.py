from fastapi import FastAPI
from app.configuration.model_config import (
    LessonRequest,
    LessonResponse
)

from app.chains.lesson_generator import LessonGenerator

app = FastAPI(
    title="AI Lesson Planner"
)

generator = LessonGenerator()


@app.get("/")
def health_check():
    return {"status": "running"}


@app.post("/generate-lesson", response_model=LessonResponse)
def generate_lesson(request: LessonRequest):

    results = generator.generate_full_lesson(
        topic=request.topic,
        grade_level=request.grade_level,
        curriculum=request.curriculum,
        dimensions=request.dimensions
    )

    return LessonResponse(results=results)