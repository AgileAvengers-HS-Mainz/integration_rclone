"""Custom integration to integrate integration_rclone with Home Assistant.

For more details about this integration, please refer to
https://github.com/AgileAvengers-FH-Mainz/integration_rclone
"""
from __future__ import annotations
import json

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import requests

from .api import IntegrationRcloneApiClient
from .const import DOMAIN
from .coordinator import RcloneDataUpdateCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]


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

def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    # Getting tasks data
    tasks_data = get_tasks_data()

    # Creating a service for each task
    create_handlers(tasks_data)

    def handle_hello(call):
        """Handle the service call."""

    # Registering the services
    hass.services.register(DOMAIN, "hello", handle_hello)
    for task in tasks_data:
        hass.services.register(DOMAIN, task["name"], "handle_" + task["name"])

    # Return boolean to indicate that initialization was successful.
    return True

def get_tasks_data():
    """Get tasks data using API"""

    # API-endpoint
    url = "http://192.168.178.65:3000/api/tasks"

    # Sending get request and saving the response as response object
    response = requests.get(url)

    # Parsing the json content into a list
    parsed_tasks_data = json.loads(response.text)

    # Replacing any spaces with underscores in each task name
    for task in parsed_tasks_data:
        task["name"] = task["name"].replace(' ', '_')

    return parsed_tasks_data

# Creating service handlers dynamically usinc exec and globals()
# It's generally not recommended due to security risks associated with
# executing arbitrary code. However, I will go for this approach for now.
def create_handlers(list_of_tasks):
    for task in list_of_tasks:
        # Define the function string using task name
        function_string = f"def handle_{task['name']}(call):\n    print('Hello!')"

        # Execute the function string
        exec(function_string, globals())
