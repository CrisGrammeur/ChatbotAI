from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "chatbot-api"
    PROJECT_VERSION: str = "1.0.0"
    SECRET_KEY: str = "323f8b82ea0876833719cb1ed317c109e9ecc868e1051e5d22b82f8fd7ce6796"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 2880

settings = Settings()