DOMAIN = "tasks_service"


import requests
from task import Task


ATTR_NAME = "name"
DEFAULT_NAME = "Standing"

# Getting the tasks data from the backend using a get request on /tasks Endpoint
# api-endpoint
URL = "http://localhost:3000/api/tasks"

# sending get request and saving the response as response object
response = requests.get(url = URL)

# extracting data in json format
tasksData: Task = response.json()

# Replacing any spaces with underscores in each task name
for task in tasksData:
    task["name"] = task["name"].replace(' ', '_')

def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    def handle_hello(call):
        """Handle the service call."""
        name = call.data.get(ATTR_NAME, DEFAULT_NAME)

        hass.states.set("tasks_service.hello", name)

    hass.services.register(DOMAIN, "hello", handle_hello)
    for task in tasksData:
        hass.services.register(DOMAIN, task["name"], "handle_" + task["name"])

    # Return boolean to indicate that initialization was successful.
    return True


# Creating functions dynamically with names based on the elements of the data list.
# It's generally not recommended due to security risks associated with
# executing arbitrary code. However, I will go for this approach for now.
def create_functions_with_exec(listOfTasks):
    for task in listOfTasks:
        # Define the function string using task name
        function_string = f"def handle_{task['name']}(call):\
            name = call.data.get(ATTR_NAME, DEFAULT_NAME)\
            hass.states.set('tasks_service.{task['name']}', name)"
        # Execute the function string
        exec(function_string, globals())
