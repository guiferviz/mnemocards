from pydantic import BaseSettings


class Settings(BaseSettings):
    recipe_filename: str = "mnemocards"

    class Config:
        env_prefix = "mnemocards_"
