from fastapi import FastAPI
from task_routers import task_router
from user_routers import user_router


app = FastAPI()

app.include_router(task_router)
app.include_router(user_router)