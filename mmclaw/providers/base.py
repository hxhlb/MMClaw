class BaseProvider(object):
    supports_native_tools = False

    def __init__(self, config):
        self.config = config
        self.engine_type = config["engine_type"]
        engine_config = config["engines"][self.engine_type]
        self.api_key = engine_config.get("api_key", "")
        self.base_url = engine_config.get("base_url", "").rstrip("/")
        self.model = engine_config["model"]
        self.debug = config.get("debug", False)
        self.stream = config.get("stream", True)

    def ask(self, messages, tools=None, retry=1):
        raise NotImplementedError

    def tool_result_messages(self, tool_calls, results):
        messages = []
        for call, result in zip(tool_calls, results):
            messages.append({
                "role": "user",
                "content": "Tool Output ({}):\n{}".format(call.get("name"), result),
            })
        return messages
