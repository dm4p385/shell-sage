import asyncio
import ollama  # Ollama for local LLM

class LLMCompletion:
    def __init__(self, ollama_model="mistral"):
        """
        Uses Ollama for local inference.

        :param ollama_model: Name of the local model (e.g., "mistral", "llama3", "my-custom-model").
        """
        self.ollama_model = ollama_model

    async def refine(self, query, candidates, top_k=5):
        """Uses Ollama asynchronously to refine and rank command suggestions."""
        if not candidates:
            return []

        prompt = f"""
            You are a highly intelligent CLI assistant that helps users autocomplete terminal commands. 
            The user input may contain typos, missing arguments, or incomplete commands.

            Given the user's input: **'{query}'**, rank and refine these possible command suggestions:

            {candidates}

            ### Instructions:
            1️⃣ **Fix any typos** in the user's input.
            2️⃣ **Prioritize commonly used commands** over rare ones.
            3️⃣ **Favor shorter, more precise completions**.
            4️⃣ **Preserve the intended meaning** of the command.
            5️⃣ **Format responses as a Python list**, e.g.:
               ["docker run -it ubuntu", "docker ps -a", "docker build -t myimage"]

            Return **only** the commands as a list and nothing else, with the most relevant at the front.
        """

        try:
            response = await asyncio.to_thread(
                ollama.chat,
                model=self.ollama_model,
                messages=[{"role": "user", "content": prompt}]
            )

            refined_suggestions = response["message"]["content"].strip()
            refined_list = eval(refined_suggestions)  # Convert string response to Python list

            if isinstance(refined_list, list):
                return refined_list[:top_k]  # Return only the top_k results
            else:
                return candidates[:top_k]  # Fallback to original suggestions if parsing fails

        except Exception as e:
            print(f"[ERROR] Ollama inference failed: {e}")
            return candidates[:top_k]  # Fallback to existing suggestions
