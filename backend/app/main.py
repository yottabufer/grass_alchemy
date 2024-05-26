from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.api.routers.tasks import router as tasks_router
from app.config import settings
from app.database import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url='/api/docs')


# Для первичной проверки, что всё работает, до миграций алембика
@app.get('/')
async def root():
    return {'message': 'Hello World'}


app.include_router(tasks_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', reload=True, port=8000)
