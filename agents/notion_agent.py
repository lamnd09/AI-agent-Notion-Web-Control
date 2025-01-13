# notion_agent.py
from langsmith import traceable
from langchain.llms.base import LLM
from langchain.schema import HumanMessage
import requests
import json
from tools.notion_browser import NotionBrowserAgent

class OllamaLlamaWrapper(LLM):
    # Fields for model configuration
    server_url: str = "http://localhost:11434/api"
    model_name: str = "llama3.2"

    @property
    def _llm_type(self) -> str:
        return "custom_ollama_llama"

    def _call(self, prompt: str, stop: list[str] | None = None) -> str:
        """
        Sends a prompt to the Ollama server and retrieves the full streamed response.
        """
        data = {"prompt": prompt, "model": self.model_name}
        try:
            # Enable streaming
            response = requests.post(f"{self.server_url}/generate", json=data, stream=True)
            response.raise_for_status()

            full_response = ""
            # Iterate over the streamed lines
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        chunk = json.loads(line)
                    except json.JSONDecodeError:
                        continue  # Skip lines that aren't valid JSON
                    # Accumulate text from each chunk
                    full_response += chunk.get("response", "")
                    # Optional: Break early if done signal received
                    if chunk.get("done", False):
                        break

            return full_response.strip() or "No response received."
        except requests.RequestException as e:
            raise RuntimeError(f"Error communicating with Ollama server: {e}") from e
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Error parsing JSON response: {e}") from e

    def generate(self, prompt: str) -> str:
        """
        Convenience method to generate a response from a prompt.
        """
        return self._call(prompt)

    def invoke(self, messages, *args, **kwargs):
        """
        Combine a list of messages into a single prompt and get the response.
        Additional arguments are accepted to maintain compatibility with external calls.
        """
        # Combine messages into a single prompt text.
        combined_prompt = "\n".join([msg.content for msg in messages])
        response_text = self._call(combined_prompt)
        # Wrap the response text into a HumanMessage.
        return HumanMessage(content=response_text)

    def bind_tools(self, tool_classes):
        """Dummy implementation of bind_tools to satisfy agent requirements."""
        return self

# Initialize the Llama3.2 wrapper instance
llama = OllamaLlamaWrapper(
    server_url="http://localhost:11434/api",
    model_name="llama3.2"
)

# Initialize the browser automation agent
browser_agent = NotionBrowserAgent()

@traceable(run_type="llm", name="Browser Notion Agent")
def handle_browser_task(command: str):
    """
    Handle user commands to interact with Notion via the browser.

    Args:
        command (str): The user command.
    Returns:
        str: The result or output of the executed command.
    """
    try:
        # Use Llama3.2 to determine the intent
        prompt = f"""
        You are an AI assistant for controlling Notion through a browser. Analyze the following command and decide the appropriate action:
        Command: "{command}"
        Possible actions: 
        1. Add a task to the Notion page.
        2. Retrieve all tasks from the Notion page.
        3. Invalid command.
        Respond with: 
        - Action: [Add Task/Get Tasks/Invalid]
        - Task: [Task description, if applicable]
        """
        response = llama.generate(prompt)
        print(f"Llama3.2 Response: {response}")

        # Parse the response (basic parsing logic; improve as needed)
        if "Add Task" in response:
            # Extract the task description after "Task:"
            parts = response.split("Task:", 1)
            task = parts[1].strip() if len(parts) > 1 else "Unnamed Task"
            page_url = "https://www.notion.so/1782eb16a9c380ecae16dc885bc4c71b?v=1782eb16a9c380f38e0f000c1126db76"  # Replace with your Notion page URL
            browser_agent.add_task(page_url, task)
            return f"Task '{task}' added to Notion."
        elif "Get Tasks" in response:
            page_url = "https://www.notion.so/1782eb16a9c380ecae16dc885bc4c71b?v=1782eb16a9c380f38e0f000c1126db76"  # Replace with your Notion page URL
            tasks = browser_agent.get_tasks(page_url)
            tasks_display = ', '.join(tasks) if tasks else "No tasks found."
            return f"Tasks retrieved: {tasks_display}"
        else:
            return "Invalid command. Please try again."
    except Exception as e:
        return f"An error occurred: {str(e)}"
