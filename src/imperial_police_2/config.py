from pydantic import Field

from pydantic_config import SettingsModel, SettingsConfig

ENV_PREFIX = "IMPERIAL_POLICE_2_"


class ImperialPoliceSettings(SettingsModel):
    model_config = SettingsConfig(
        env_prefix=ENV_PREFIX,
    )

    # Postgres settings
    POSTGRES_HOST: str = Field()
    POSTGRES_PORT: int = Field()
    POSTGRES_USER: str = Field()
    POSTGRES_PASSWORD: str = Field()
