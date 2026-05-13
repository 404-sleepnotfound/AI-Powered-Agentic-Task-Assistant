import google.generativeai as genai
import json
import os

API_KEY =  "YOUR_API_KEY_HERE"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "gemini-flash-lite-latest"
)

class AgenticAssistant:

    def __init__(self):

        self.tasks = []

        self.load_tasks()


    def load_tasks(self):

        if os.path.exists("tasks.json"):

            with open("tasks.json", "r") as file:

                self.tasks = json.load(file)


    def save_tasks(self):

        with open("tasks.json", "w") as file:

            json.dump(self.tasks, file, indent=4)

    def create_goal(self, goal):

        print(f"\nGoal Received: {goal}\n")

        prompt = f"""
        Break this goal into actionable tasks.

        Goal: {goal}

        Return in this exact format:

        Task: ...
        Description: ...
        Difficulty: Easy/Medium/Hard

        Keep tasks concise.
        """

        try:

            print("Generating AI tasks...\n")

            response = model.generate_content(prompt)

            generated_text = response.text

        except Exception as e:

            print("\nAI Error:")
            print(e)

            return

        lines = generated_text.split("\n")

        self.tasks.clear()

        task = {}

        priority = 1

        for line in lines:

            line = line.strip()

            if line.startswith("Task:"):

                if task:

                    task["priority"] = priority
                    task["completed"] = False

                    self.tasks.append(task)

                    priority += 1

                task = {
                    "task": line.replace("Task:", "").strip()
                }

            elif line.startswith("Description:"):

                task["description"] = line.replace(
                    "Description:",
                    ""
                ).strip()

            elif line.startswith("Difficulty:"):

                task["difficulty"] = line.replace(
                    "Difficulty:",
                    ""
                ).strip()


        if task:

            task["priority"] = priority
            task["completed"] = False

            self.tasks.append(task)

        self.save_tasks()

        print("AI-generated tasks created successfully!\n")


    def show_tasks(self):

        print("\n========== TASK LIST ==========\n")

        if len(self.tasks) == 0:

            print("No tasks available.\n")

            return

        for i, task in enumerate(self.tasks):

            status = (
                "Done"
                if task["completed"]
                else "Pending"
            )

            print(f"{i + 1}. {task['task']}")

            print(
                f"   Description: "
                f"{task['description']}"
            )

            print(
                f"   Difficulty: "
                f"{task['difficulty']}"
            )

            print(
                f"   Priority: "
                f"{task['priority']}"
            )

            print(f"   Status: {status}\n")


    def complete_task(self, index):

        if 0 <= index < len(self.tasks):

            self.tasks[index]["completed"] = True

            self.save_tasks()

            print("\nTask marked as completed!")

            self.show_progress()

        else:

            print("\nInvalid task number!")


    def show_progress(self):

        if len(self.tasks) == 0:

            print("\nNo tasks available.")

            return

        completed = sum(
            1 for task in self.tasks
            if task["completed"]
        )

        total = len(self.tasks)

        percent = (completed / total) * 100

        print(
            f"\nProgress: "
            f"{percent:.0f}% completed\n"
        )


    def suggest_next_task(self):

        pending_tasks = [

            task for task in self.tasks

            if not task["completed"]

        ]

        if pending_tasks:

            next_task = min(
                pending_tasks,
                key=lambda x: x["priority"]
            )

            print("\n===== NEXT BEST TASK =====\n")

            print(
                f"Task: {next_task['task']}"
            )

            print(
                f"Description: "
                f"{next_task['description']}"
            )

            print(
                f"Difficulty: "
                f"{next_task['difficulty']}\n"
            )

        else:

            print("\nAll tasks completed!\n")


assistant = AgenticAssistant()

print("===================================")
print("   AI AGENTIC TASK ASSISTANT")
print("===================================")

while True:

    print("\n=========== MENU ===========")

    print("1. Create Goal")
    print("2. Show Tasks")
    print("3. Complete Task")
    print("4. Show Progress")
    print("5. Suggest Next Task")
    print("6. Exit")

    choice = input("\nEnter choice: ")

    if choice == "1":

        goal = input("\nEnter your goal: ")

        assistant.create_goal(goal)

    elif choice == "2":

        assistant.show_tasks()

    elif choice == "3":

        try:

            num = int(
                input(
                    "\nEnter task number to complete: "
                )
            )

            assistant.complete_task(num - 1)

        except:

            print("\nInvalid input!")

    elif choice == "4":

        assistant.show_progress()

    elif choice == "5":

        assistant.suggest_next_task()

    elif choice == "6":

        print("\nExiting program...")

        break

    else:

        print("\nInvalid choice!")