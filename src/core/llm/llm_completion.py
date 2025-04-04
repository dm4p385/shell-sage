import json
import ollama
import asyncio


class LLMCompletion:
    def __init__(self, ollama_model="mistral"):
        self.ollama_model = ollama_model

    async def refine(self, query, candidates, top_k=5):
        if not candidates:
            return []

        system_prompt = (
            "You are a CLI autocompletion assistant. Your job is to suggest refined and corrected command-line completions.\n"
            "You NEVER include any explanation, markdown, or code blocks.\n"
            "You ALWAYS respond ONLY with a strict JSON list of strings.\n"
            "Each suggestion must be short, correct, and useful in a terminal.\n"
            "Return exactly 3 completions. If unsure, still provide best guesses."
            "Focus more on completing the current word and predicting the next word"
        )

        user_prompt = f"""
        The user typed: '{query}'

        Here are some possible completions: {candidates}
        
        Now respond with a JSON list of 3 refined suggestions. Do not include explanations or formatting.
        Focus more on completing the current word and predicting the next word rather than providing a complete command
        Example:
        ["docker run -it ubuntu", "docker ps -a", "docker build -t myapp ."]
        """

        try:
            # Run in background thread to avoid blocking asyncio loop
            response = await asyncio.to_thread(
                ollama.chat,
                model=self.ollama_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            )

            raw_output = response["message"]["content"].strip()
            print(f"[DEBUG] Raw output: {raw_output}")

            # Try to parse as JSON
            refined = json.loads(raw_output)
            return refined[:top_k] if isinstance(refined, list) else candidates[:top_k]

        except Exception as e:
            print(f"[ERROR] LLM refine failed: {e}")
            return candidates[:top_k]
