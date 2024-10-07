from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.project import router as project_router
from app.routes.task import router as task_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешенные источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)


# Подключение роутеров
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(project_router, prefix="/projects", tags=["Projects"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])