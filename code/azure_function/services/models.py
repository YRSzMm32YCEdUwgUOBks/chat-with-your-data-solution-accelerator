import os
from typing import Dict
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
        provider = model_cfg.provider.lower()
        if provider == "azureopenai":
            conf = model_cfg.config
            deployment = os.getenv(conf.get("azureopenai_deployment_env"))
            endpoint = os.getenv(conf.get("azureopenai_endpoint_env"))
            api_key = os.getenv(conf.get("azureopenai_api_key_env"))
            # model can be directly specified or via env
            model = conf.get("model") or os.getenv(conf.get("azureopenai_model_env"))
            api_version = conf.get("azureopenai_api_version")
            return AzureOpenAIChatCompletionClient(
                azure_deployment=deployment,
                model=model,
                api_version=api_version,
                azure_endpoint=endpoint,
                azure_ad_token_provider=None,
                api_key=api_key,
            )
        # TODO: add support for other providers (openai, ollama, anthropic, etc.)
        raise NotImplementedError(f"Provider '{model_cfg.provider}' not implemented")
