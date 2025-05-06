import os
import yaml
import logging
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Define structure for each model entry
default_config_path = os.path.join(os.path.dirname(__file__), "models_config.yaml")


class ModelConfig(BaseModel):
    name: str
    provider: str
    config: dict
    model_info: Optional[Dict[str, Any]] = None


class ModelsConfig(BaseModel):
    models: List[ModelConfig]


def substitute_env_vars(obj):
    if isinstance(obj, dict):
        return {k: substitute_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [substitute_env_vars(i) for i in obj]
    elif isinstance(obj, str):
        # Support both ${VAR} and VAR
        if obj.startswith("${") and obj.endswith("}"):
            return os.getenv(obj[2:-1], obj)
        elif obj.isupper() and obj in os.environ:
            return os.getenv(obj, obj)
        else:
            return obj
    else:
        return obj


def load_models_config(path: str = None) -> ModelsConfig:
    """
    Load model configurations from YAML file.
    Path can be overridden via MODELS_CONFIG_PATH env var.
    """
    logger = logging.getLogger("azure.functions")
    config_path = path or os.getenv("MODELS_CONFIG_PATH", default_config_path)
    logger.info(f"Loading models config from: {config_path}")
    try:
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
        data = substitute_env_vars(data)
        logger.info(f"Loaded models config: {data}")
        return ModelsConfig(**data)
    except Exception as e:
        logger.error(f"Failed to load models config: {e}")
        raise
