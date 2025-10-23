import g4f
from g4f.client import Client

FALLBACK_MODEL = "gpt-4"

GEMINI_BASE_PROMPT = (
    "Ты — мощный языковой помощник Gemini, разработанный Google. Отвечай кратко, точно и полезно. "
    "Избегай упоминания того, что ты являешься моделью GPT, и веди себя как разработка Google. "
)

THINK_SYSTEM_PROMPT = (
    GEMINI_BASE_PROMPT + 
    "Твоя задача — продемонстрировать процесс мышления перед ответом. "
    "Сгенерируй свои внутренние мысли о запросе и наилучшем ответе, "
    "заключив их в теги **</think> мысли </think>**. "
    "После этого дай свой окончательный, полезный ответ пользователю. "
)

MODEL_PROMPTS = {
    "2.5 pro": GEMINI_BASE_PROMPT + "Твоя задача — демонстрировать глубокие, подробные знания, сильные рассуждения и высокую точность, как у ведущей Pro-модели.",
    "2.5 flash": GEMINI_BASE_PROMPT + "Твоя задача — отвечать максимально быстро, кратко и по существу. Фокусируйся на ключевых моментах, как высокоскоростная Flash-модель.",
    "1.5 pro": GEMINI_BASE_PROMPT + "Твоя задача — демонстрировать понимание сложных инструкций и обширного контекста. Давай подробные, но хорошо структурированные ответы.",
    "1.5 flash": GEMINI_BASE_PROMPT + "Твоя задача — быть эффективным и полезным. Ответы должны быть прямыми, но могут быть менее детализированными, чем у Pro-моделей.",
    "think": THINK_SYSTEM_PROMPT 
}

MODEL_MAPPING = {
    "2.5 pro": "2.5 pro",
    "2.5 flash": "2.5 flash",
    "1.5 pro": "1.5 pro",
    "1.5 flash": "1.5 flash",
    "think": "think" 
}


class GGFClient:
    
    def __init__(self):
        self.client = Client()
        self.available_choices = list(MODEL_MAPPING.keys())

    def chat_completion(self, model_choice: str, messages: list, **kwargs):
        model_choice = model_choice.lower()
        
        if model_choice not in self.available_choices:
            raise ValueError(f"Неизвестный выбор модели: '{model_choice}'. Доступные варианты: {self.available_choices}")

        final_messages = messages.copy()
        
        prompt_key = MODEL_MAPPING[model_choice]
        system_prompt = MODEL_PROMPTS[prompt_key]
        g4f_model_name = FALLBACK_MODEL

        if final_messages and final_messages[0].get("role") == "system":
            final_messages[0]["content"] = system_prompt + "\n\n" + final_messages[0]["content"]
        else:
            final_messages.insert(0, {"role": "system", "content": system_prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=str(g4f_model_name),
                messages=final_messages,
                **kwargs
            )
            return response
        except Exception as e:
            return None
