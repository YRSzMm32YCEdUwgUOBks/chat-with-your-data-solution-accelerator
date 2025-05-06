import os
from typing import Dict
from dataclasses import asdict, is_dataclass
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from .models_config import load_models_config, ModelsConfig, ModelConfig


def create_model_factory() -> "ModelClientFactory":
    config = load_models_config()
    return ModelClientFactory(config)


class ModelClientFactory:
    """
    Factory to instantiate and cache model clients based on configuration.
    """

    def __init__(self, config: ModelsConfig):
        self._config = config
        self._clients: Dict[str, object] = {}

    def get_client(self, name: str):
        # Return existing client if already created
        if name in self._clients:
            return self._clients[name]
        # Find model config by name
        model_cfg = next((m for m in self._config.models if m.name == name), None)
        if not model_cfg:
            raise ValueError(f"Model config '{name}' not found")
        client = self._create_client(model_cfg)
        self._clients[name] = client
        return client

    def _create_client(self, model_cfg: ModelConfig):
        import logging

        logger = logging.getLogger("azure.functions")
        provider = model_cfg.provider.lower()
        if provider == "azureopenai":
            conf = model_cfg.config
            deployment = os.getenv(conf.get("azure_openai_deployment_env"))
            endpoint = os.getenv(conf.get("azure_openai_endpoint_env"))
            api_key = os.getenv(conf.get("azure_openai_api_key_env"))
            model = os.getenv(conf.get("azure_openai_model_env"))
            api_version = os.getenv(conf.get("azure_openai_api_version_env"))
            # Ensure model_info is a dict
            if getattr(model_cfg, "model_info", None) is not None:
                if is_dataclass(model_cfg.model_info):
                    model_info = asdict(model_cfg.model_info)
                elif isinstance(model_cfg.model_info, dict):
                    model_info = model_cfg.model_info
                else:
                    model_info = dict(model_cfg.model_info)
            else:
                model_info = None
            logger.info(
                f"AzureOpenAIChatCompletionClient args: model={model}, deployment={deployment}, endpoint={endpoint}, api_version={api_version}, api_key={'set' if api_key else 'unset'}, model_info={model_info}"
            )
            return AzureOpenAIChatCompletionClient(
                azure_deployment=deployment,
                model=model,
                api_version=api_version,
                azure_endpoint=endpoint,
                azure_ad_token_provider=None,
                api_key=api_key,
                model_info=model_info,
            )
        # TODO: add support for other providers (openai, ollama, anthropic, etc.)
        raise NotImplementedError(f"Provider '{model_cfg.provider}' not implemented")
