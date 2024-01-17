"""Custom integration to integrate integration_rclone with Home Assistant.

For more details about this integration, please refer to
https://github.com/AgileAvengers-FH-Mainz/integration_rclone
"""
from __future__ import annotations
import json
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

import requests
import time
from homeassistant.core import callback


from .api import IntegrationRcloneApiClient
from .const import DOMAIN
from .coordinator import RcloneDataUpdateCoordinator



PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]

CONF_URL = "url"

STATE_RUNNING = "Running"
STATE_DONE = "Done"

WAIT_SECONDS = 5

# Checking if all mandatory configuration variables are provided ('url' in our case).
# If not, the setup of our integration should fail.
# We use voluptuous as a helper to achieve this.
CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({vol.Required(CONF_URL): cv.string,})}, extra=vol.ALLOW_EXTRA
)


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator = RcloneDataUpdateCoordinator(
        hass=hass,
        client=IntegrationRcloneApiClient(
            username=entry.data[CONF_USERNAME],
            password=entry.data[CONF_PASSWORD],
            session=async_get_clientsession(hass),
        ),
    )
    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)

# Registering new services in the integration using the setup function.
# Services can be called from automations and from the service "Developer tools" in the frontend.
def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    # This service can be called to trigger a reload of the configuration,
    # allowing dynamic updates without the need for restarting the application.
    def handle_reload_config(call):
        setup(hass, config)

    hass.services.register(DOMAIN, "reload_config", handle_reload_config)

    # API-endpoint from the configuration.yaml file
    url = config[DOMAIN].get(CONF_URL)

    # Getting tasks data
    tasks_data = get_tasks_data(url)

    # Creating a service for each task
    create_handlers(tasks_data, url)

    # Registering the services
    register_services(hass, tasks_data)

    # Return boolean to indicate that initialization was successful.
    return True

def register_services(hass, list_of_tasks):
    """Register a service for each task."""

    for task in list_of_tasks:
        hass.services.register(DOMAIN, task["name"],
                               globals()["handle_" + task["name"]])

def create_handlers(list_of_tasks, url):
    """Create service handlers dynamically for each task usinc exec and globals().

    It's generally not recommended due to security risks associated with
    executing arbitrary code. However, I will go for this approach for now.
    Args:
        list_of_tasks: A list of json objects of tasks.
    """
    for task in list_of_tasks:
        # Define the function string using task name
        function_string = f"def handle_{task['name']}(call):\n\
            exec_task({task}, '{url}')"

        # Execute the function string
        exec(function_string, globals())

def exec_task(task, url):
    """Call when the task is executed.

    This methode is used to simplify the function string.
    Args:
        task: Json object of a task.
    """
    logging.info(f"Executing Task, id: {task['id']}, name: {task['name']}")

    try:
        response = requests.post(f"{url}/api/tasks/{task['id']}/run")
        logging.info(f"Task done. Response: " + response.text)
    except Exception as error:
        logging.error(f"Something went wrong. Error: " + error)

def get_tasks_data(url):
    """Get tasks data using API.

    Args:
        url: The URL of the Endpoint-API.
    """

    # Sending get request and saving the response as response object
    response = requests.get(url)

    # Parsing the json content into a list
    parsed_tasks_data = json.loads(response.text)

    # Replacing any spaces with underscores in each task name
    # and making sure they are all in lower case
    for task in parsed_tasks_data:
        task["name"] = task["name"].replace(' ', '_').lower()

    return parsed_tasks_data
