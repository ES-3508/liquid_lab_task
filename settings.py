from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Stock Summary API"
    alphavantage_api_key: str
    db: str

    class Config:
        env_file = ".env"


settings = Settings()