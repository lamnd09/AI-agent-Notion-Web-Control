# tests/test_notion_browser.py
import os
from tools.notion_browser import NotionBrowserAgent

def main():
    # Replace these with your actual Notion credentials and page URL.
    email = "your-email@example.com"
    password = "YourSecurePassword"
    notion_page_url = "https://www.notion.so/YourWorkspace/YourPageName-abc123def456"  # Replace with your Notion page URL.
    
    agent = NotionBrowserAgent()
    
    try:
        # Log in if state file doesn't exist
        if not os.path.exists("notion_state.json"):
            agent.login_to_notion(email, password)
        
        test_task = "Test Task from Automation"
        agent.add_task(notion_page_url, test_task)
        
        tasks = agent.get_tasks(notion_page_url)
        print("Tasks on the page:", tasks)
        
    except Exception as e:
        print("An error occurred:", e)
    finally:
        agent.close()

if __name__ == "__main__":
    main()
