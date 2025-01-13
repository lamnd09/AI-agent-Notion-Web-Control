# main.py
import os
from tools.notion_browser import NotionBrowserAgent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    # Load credentials and configuration from environment variables
    email = os.getenv("NOTION_EMAIL")
    password = os.getenv("NOTION_PASSWORD")
    project_url = os.getenv("NOTION_PAGE_URL")

    if not all([email, password, project_url]):
        print("Missing required environment variables. Please set NOTION_EMAIL, NOTION_PASSWORD, and NOTION_PAGE_URL.")
        return

    # Initialize the browser agent
    agent = NotionBrowserAgent()

    try:
        # Log in to Notion
        print("Logging into Notion...")
        agent.login_to_notion(email, password)
        print("Logged in successfully.")

        # Navigate to the project page
        print(f"Navigating to the project page: {project_url}")
        agent.navigate_to_project(project_url)
        print("Navigation complete.")

        # Add tasks
        for i in range(1, 6):  # Example: Add 5 tasks
            task_name = f"task {i}"
            print(f"Adding task: {task_name}")
            agent.add_task(task_name)

        print("All tasks added successfully. The browser will remain open for further actions.")

    except Exception as e:
        print(f"An error occurred: {e}")

    # Do not close the browser to allow manual interaction.
    print("You can manually interact with the browser. Close it when you're done.")

if __name__ == "__main__":
    main()
