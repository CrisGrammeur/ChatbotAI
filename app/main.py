from config.settings import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from config.database import engine, Base
from routers import user_route
# import uvicorn

origins = ["*"]
Base.metadata.create_all(engine)

def include_router(app):
    app.include_router(user_route)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    include_router(app)
    # create_tables()
    return app

app = start_application()

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)