# tools/notion_browser.py
import time
from playwright.sync_api import sync_playwright

class NotionBrowserAgent:
    def __init__(self):
        self.playwright = sync_playwright().start()
        # Launch browser in non-headless mode for visible window/tab
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def login_to_notion(self, email: str, password: str):
        """
        Log into Notion using the provided credentials.
        """
        self.page.goto("https://www.notion.so/login")
        
        email_selector = "input[placeholder='Enter your email address...']"
        self.page.wait_for_selector(email_selector)
        self.page.fill(email_selector, email)
        self.page.keyboard.press("Enter")
        
        password_selector = "input[type='password']"
        self.page.wait_for_selector(password_selector)
        self.page.fill(password_selector, password)

        # Wait for and click the "Continue with password" button
        continue_button_selector = 'div[role="button"]:has-text("Continue with password")'
        self.page.wait_for_selector(continue_button_selector)
        self.page.click(continue_button_selector)
        
        self.page.wait_for_load_state("networkidle")
        time.sleep(5)  # Additional wait to ensure session stability
        print("Logged into Notion.")

    def navigate_to_project(self, project_url: str):
        """
        Navigate to the specified Notion project page.
        """
        self.page.goto(project_url)
        self.page.wait_for_load_state("networkidle")
        time.sleep(2)  # Wait to ensure the page is fully loaded
        print("Navigated to project page.")

    def add_task(self, task_name: str):
        """
        Add a new task to the project page.
        """
       
        # Selector for the "New" button inside the container
        new_button_selector = 'div[role="button"]:has-text("New")'

        # Click the "New" button to add a task
        self.page.wait_for_selector(new_button_selector)
        self.page.click(new_button_selector)

        # Selector for the task name input field
        task_input_selector = 'h1[placeholder="New task"]'
        self.page.wait_for_selector(task_input_selector)

        # Fill the task name
        self.page.fill(task_input_selector, task_name)
        self.page.keyboard.press("Enter")
        print(f"Added task: {task_name}")

    def close(self):
        self.browser.close()
        self.playwright.stop()
