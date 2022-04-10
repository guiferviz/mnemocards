from pydantic import BaseSettings


class Settings(BaseSettings):
    """Global mnemocards settings.

    All the properties of this class can be overwritten by environment variables
    with the "MNEMOCARDS_" prefix. For example, if you want to use a different
    recipe_filename you can run mnemocards using the following command:
    `MNEMOCARDS_RECIPE_FILENAME=my_new_recipe_name mnemocards cook`.
    """

    recipe_filename: str = "mnemocards"

    class Config:
        env_prefix = "mnemocards_"
