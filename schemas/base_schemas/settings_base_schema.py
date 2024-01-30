from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Scripts API"
    admin_email: str = "lilko.petkovv@gmail.com"
