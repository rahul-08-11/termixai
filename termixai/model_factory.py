from termixai.utils.config import get_model_config
from termixai.models.openai_model import OpenAIModel
from termixai.models.azure_model import AzureOpenAIModel
from termixai.models.gemini_model import GeminiModel
class ModelFactory:
    @staticmethod
    async def create(model_name):
        model_detials = get_model_config(model_name)
        provider = model_detials["provider"]
        if provider == "openai":
            return await OpenAIModel(**model_detials)

        elif provider == "azure":
            return AzureOpenAIModel(
                **model_detials
            )

        elif provider == "gemini":
            return await GeminiModel(**model_detials)

        else:
            raise ValueError(f"Unknown provider: {provider}")
