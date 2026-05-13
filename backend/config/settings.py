from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    gemini_api_key: str
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    dynamodb_table_name: str
    s3_bucket_name: str
    allowed_origins: str

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]


settings = Settings()