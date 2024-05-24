from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    echo_sql: bool = True
    test: bool = False
    project_name: str = "grass"
    oauth_token_secret: str = "grass"
    log_level: str = "DEBUG"


settings = Settings()
