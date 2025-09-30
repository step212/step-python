from typing import Any, List, Optional, Union

from pydantic import AnyHttpUrl, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[Union[AnyHttpUrl, str]] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    @field_validator("BACKEND_CORS_ORIGINS")
    def validate_cors_origins(cls, v: List[Union[AnyHttpUrl, str]]) -> List[Union[AnyHttpUrl, str]]:
        validated_origins = []
        for origin in v:
            if isinstance(origin, str):
                # Allow "*" as a special wildcard value for CORS
                if origin == "*":
                    validated_origins.append(origin)
                else:
                    # Try to validate as URL, if it fails, keep as string for flexibility
                    try:
                        validated_origins.append(AnyHttpUrl(origin))
                    except:
                        validated_origins.append(origin)
            else:
                validated_origins.append(origin)
        return validated_origins

    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DATABASE: str
    DATABASE_URI: Optional[str] = None

    @field_validator("DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return f"mysql://{info.data['MYSQL_USER']}:{info.data['MYSQL_PASSWORD']}@{info.data['MYSQL_HOST']}:" \
               f"{info.data['MYSQL_PORT']}/{info.data['MYSQL_DATABASE']}"
    
    DEEPSEEK_API_KEY: str

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
