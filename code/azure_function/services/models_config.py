import os
import yaml
from pydantic import BaseModel
from typing import List

# Define structure for each model entry
default_config_path = os.path.join(os.path.dirname(__file__), "models_config.yaml")


class ModelConfig(BaseModel):
    name: str
    provider: str
    config: dict


class ModelsConfig(BaseModel):
    models: List[ModelConfig]


def load_models_config(path: str = None) -> ModelsConfig:
    """
    Load model configurations from YAML file.
    Path can be overridden via MODELS_CONFIG_PATH env var.
    """
    config_path = path or os.getenv("MODELS_CONFIG_PATH", default_config_path)
    with open(config_path, "r") as f:
        data = yaml.safe_load(f)
    return ModelsConfig(**data)
