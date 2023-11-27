DOMAIN = "tasks_service"


""" ATTR_ID = "id"
DEFAULT_ID = "DEFAULT_ID" """

ATTR_NAME = "name"
DEFAULT_NAME = "Standing"

""" ATTR_TYPE = ""
DEFAULT_TYPE = "DEFAULT_TYPE"

ATTR_DESCRIPTION = ""
DEFAULT_DESCRIPTION = "DEFAULT_DESCRIPTION"

ATTR_SOURCE_PATH = ""
DEFAULT_SOURCE_PATH = "DEFAULT_SOURCE_PATH"

ATTR_SOURCE_TYPE = ""
DEFAULT_SOURCE_TYPE = "DEFAULT_SOURCE_TYPE"

ATTR_DESTINATION_PATH = ""
DEFAULT_DESTINATION_PATH = "DEFAULT_DESTINATION_PATH"

ATTR_DESTINATION_TYPE = ""
DEFAULT_DESTINATION_TYPE = "DEFAULT_DESTINATION_TYPE" """


def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    # Creating functions dynamically with names based on the elements of a list.
    # It's generally not recommended due to security risks associated with
    # executing arbitrary code. However, I will go for this approach for now.
    def create_functions_with_exec(elements):
        for element in elements:
            # Define the function string
            function_string = f"def handle_{element}(call):\n    name = call.data.get(ATTR_NAME, DEFAULT_NAME)\n    hass.states.set('tasks_service.{element}', name)"
            # Execute the function string
            exec(function_string, globals())

    # Example list of elements
    my_list = ['apple', 'banana', 'orange']

    # Create functions based on the list elements using exec
    create_functions_with_exec(my_list)

    def handle_hello(call):
        """Handle the service call."""
        """ id = call.data.get(ATTR_ID, DEFAULT_ID) """

        name = call.data.get(ATTR_NAME, DEFAULT_NAME)

        hass.states.set("tasks_service.hello", name)

        """type = call.data.get(ATTR_TYPE, DEFAULT_TYPE)
        description = call.data.get(ATTR_DESCRIPTION, DEFAULT_DESCRIPTION)
        source_path = call.data.get(ATTR_SOURCE_PATH, DEFAULT_SOURCE_PATH)
        source_type = call.data.get(ATTR_SOURCE_TYPE, DEFAULT_SOURCE_TYPE)
        destination_path = call.data.get(ATTR_DESTINATION_PATH, DEFAULT_DESTINATION_PATH)
        destination_type = call.data.get(ATTR_DESTINATION_TYPE, DEFAULT_DESTINATION_TYPE) """

        name = call.data.get(ATTR_NAME, "done")
        hass.states.set("tasks_service.hello", name)

    hass.services.register(DOMAIN, "hello", handle_hello)
    for element in my_list:
        hass.services.register(DOMAIN, element, "handle_" + element)

    # Return boolean to indicate that initialization was successful.
    return True


def create_functions_with_exec(elements):
    for element in elements:
        # Define the function string
        function_string = f"def {element}():\n    print('This is the function for {element}')"

        # Execute the function string
        exec(function_string, globals())

# Example list of elements
my_list = ['apple', 'banana', 'orange']

# Create functions based on the list elements using exec
create_functions_with_exec(my_list)

# Now you can call the functions using their corresponding names
for element in my_list:
    print(f"Calling function for {element}:")
    globals()[element]()

    