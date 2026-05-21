from .legacy import compress_image, prepare_image_content
from .codex import CodexProvider
from .legacy import Engine as LegacyEngine
from .openai_compatible import OpenAICompatibleProvider
from .vertex_ai import VertexAIProvider


OPENAI_COMPATIBLE_NATIVE_PROVIDERS = {
    "openai",
    "google",
    "deepseek",
    "openrouter",
    "kimi",
    "kimi_ai",
    "kimi_cn",
    "minimax_io",
    "minimax_cn",
}


class LegacyProviderAdapter(object):
    supports_native_tools = False

    def __init__(self, config):
        self._engine = LegacyEngine(config)

    def ask(self, messages, tools=None, retry=1):
        return self._engine.ask(messages, tools=tools, retry=retry)

    def tool_result_messages(self, tool_calls, results):
        messages = []
        for call, result in zip(tool_calls, results):
            messages.append({
                "role": "user",
                "content": "Tool Output ({}):\n{}".format(call.get("name"), result),
            })
        return messages


class Engine(object):
    def __init__(self, config):
        self.config = config
        self.engine_type = config["engine_type"]
        self.provider = self._make_provider(config)

    def _make_provider(self, config):
        engine_type = config.get("engine_type")
        if engine_type == "codex":
            return CodexProvider(config)
        if engine_type == "vertex_ai":
            return VertexAIProvider(config)
        if engine_type in OPENAI_COMPATIBLE_NATIVE_PROVIDERS or engine_type.startswith("openai_compatible_"):
            return OpenAICompatibleProvider(config)
        return LegacyProviderAdapter(config)

    @property
    def supports_native_tools(self):
        return bool(getattr(self.provider, "supports_native_tools", False))

    def ask(self, messages, tools=None, retry=1):
        return self.provider.ask(messages, tools=tools, retry=retry)

    def tool_result_messages(self, tool_calls, results):
        return self.provider.tool_result_messages(tool_calls, results)


__all__ = ["Engine", "compress_image", "prepare_image_content"]
