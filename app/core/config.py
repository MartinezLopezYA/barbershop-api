from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore

class Settings(BaseSettings):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: str
    DATABASE: str

    @property
    def DATABASE_URL(self) -> str:
        print("DATABASE_URL")
        print(f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}")
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()