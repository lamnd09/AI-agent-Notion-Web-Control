# llama_wrapper.py
import requests

class OllamaLlamaWrapper:
    """
    Wrapper for interacting with the Ollama server's LLaMA-based models.
    """

    def __init__(self, server_url="http://localhost:11434/api", model_name="llama3.2"):
        self.server_url = server_url
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        """
        Sends a prompt to the Ollama server and retrieves the response.
        """
        data = {"prompt": prompt, "model": self.model_name}
        try:
            response = requests.post(f"{self.server_url}/generate", json=data)
            response.raise_for_status()
            resp_json = response.json()
            return resp_json.get("response", "No response received.")
        except requests.RequestException as e:
            return f"Error communicating with Ollama server: {str(e)}"
