# AI-agent-Notion-Web-Control

This project automates interactions with Notion through a browser. It logs in, navigates to a specified project page, and performs actions such as adding tasks automatically. With the integration of  **LLaMA 3.2** , the AI agent is enhanced with natural language understanding, intent recognition, and decision-making capabilities, making it more versatile and powerful.

[Video Demo](media/video_demo_web.mp4)

## Features

* **Automated Login:** Logs into Notion using user-provided credentials.

* **Project Navigation:** Navigates to a specified Notion project page URL.
* **Task Automation:** Adds tasks to the project by clicking the "New" button and filling in task details.
* **LLaMA 3.2 Integration:**
  * Understands and parses natural language commands.
  * Recognizes user intent and determines actions (e.g., "Add task", "Retrieve tasks").
  * Handles ambiguous commands by generating clarifying questions.
  * Generates detailed, human-like responses summarizing actions.
* **Browser Persistence:** Keeps the browser open for manual interactions after automation.

## Prerequisites

* **Python 3.7+** : Ensure Python is installed.
* **Playwright** : For browser automation.
* **dotenv** : For loading environment variables.
* **LLaMA 3.2** : Deployed locally or via an API for advanced NLP tasks. In this case, I leverage Ollama to run Llama3.2

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/lamnd09/AI-agent-Notion-Web-Control.git
   cd notion-automation-agent
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   playwright install
   ```
3. Create a `.env` file in the root directory with the following content:

   ```env
   NOTION_EMAIL=your-email@example.com
   NOTION_PASSWORD=YourSecurePassword
   NOTION_PAGE_URL=https://www.notion.so/1782eb16a9c380ecae16dc885bc4c71b?v=1782eb16a9c380f38e0f000c1126db76
   ```

   Replace the placeholders with your Notion credentials and project page URL.

## Usage

1. Run the script:

   ```bash
   streamlit main.py
   ```
2. * **What Happens:**
     * Logs into Notion using the provided credentials.
     * Navigates to the specified project page.
     * Uses LLaMA 3.2 to parse user commands and determine actions.
     * Executes commands automatically, such as adding tasks.
   * **Example Commands:**
     * "Add a task to finalize the project report."
     * "What are my tasks due tomorrow?"

## Project Structure

```
AI-agent-Notion-Web-Control/
├── agents/                    # Contains agents and wrappers for LLMs and Notion
│   ├── __init__.py            # Makes the directory a Python package
│   ├── llm_wrapper.py         # Wrapper for integrating with LLaMA 3.2 or similar LLMs
│   └── notion_agent.py        # Handles AI-driven interactions with Notion
├── tools/                     # Contains browser automation tools
│   ├── __init__.py            # Makes the directory a Python package
│   └── notion_browser.py      # Contains the NotionBrowserAgent class for Playwright automation
├── .env                       # Environment variables for credentials and configuration
├── app.py                     # Main script to execute the AI agent (Streamlit-based)
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies

```

### **Workflow**

1. **Command Parsing:**
   * The user inputs a natural language command (e.g., "Add a task named 'Prepare report'.").
   * LLaMA 2 analyzes the command and identifies the action (`Add task`) and the task details (`Prepare report`).
2. **Decision-Making:**
   * If the command is ambiguous, LLaMA 2 can clarify by asking follow-up questions or making intelligent assumptions.
3. **Execution:**
   * Once the command is parsed, the agent uses Playwright to execute the corresponding action on Notion.
4. **Response Generation:**
   * After executing the task, LLaMA 2 generates a detailed response for the user, summarizing the action taken.

![image](media/workflow.png)

## Example

Here’s an example of adding 5 tasks automatically:

```bash
streamlit run app.py
```

Output:

```
Logging into Notion...
Logged in successfully.
Navigating to the project page: https://www.notion.so/...
Navigation complete.
Adding task: task 1
Adding task: task 2
Adding task: task 3
Adding task: task 4
Adding task: task 5
All tasks added successfully. The browser will remain open for further actions.
```

## Dependencies

- **Playwright**: For browser automation.
- **dotenv**: For environment variable management.

## How LLaMA 3.2 Supports the Agent

1. **Natural Language Understanding:**
   LLaMA 3.2 interprets user commands and converts them into structured actions for the agent.
2. **Intent Recognition:**
   Maps natural language input to predefined intents (e.g., "Add Task", "Get Tasks").
3. **Task Management Enhancements:**
   * Summarizes tasks intelligently.
   * Prioritizes tasks based on inferred urgency or deadlines.
4. **Flexibility:**
   Handles a wide range of inputs, making the agent adaptable to different user needs.
5. **Dynamic Responses:**
   Generates detailed feedback, improving user experience.

## Notes

- Ensure your credentials and project URL are correct in the `.env` file.
- The script currently supports Chrome-based browsers and launches in non-headless mode for visibility.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

[Your Name]

For any issues or feature requests, please open an issue on the GitHub repository.
