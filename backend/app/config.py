from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TutorSlot API"
    # Local dev defaults to a zero-config SQLite file.
    # Docker Compose and Kubernetes override this with a PostgreSQL URL.
    database_url: str = "sqlite:///./tutorslot.db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
