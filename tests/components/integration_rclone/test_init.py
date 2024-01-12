"""Test integration_rclone component setup process."""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from unittest.mock import patch

from custom_components.integration_rclone import (
    async_setup_entry,
    async_unload_entry,
    setup
)

from custom_components.integration_rclone.const import DOMAIN as DOMAIN_INTEGRATION_RCLONE

async def setup_entry(hass, entry):
    """Test that setup entry works."""
    with patch("async_setup", return_value=True):
        assert await async_setup_entry(hass, entry) is True

async def test_setup(hass, config):
    """Test the component gets setup."""
    assert await setup(hass, DOMAIN_INTEGRATION_RCLONE, {}) is True

async def test_setup_entry_successful(
    hass: HomeAssistant, entry: ConfigEntry
) -> None:
    """Test setup entry is successful."""
    config_entry = await async_setup_entry(hass, entry)

    assert hass.data[DOMAIN_INTEGRATION_RCLONE]
    assert config_entry.entry_id in hass.data[DOMAIN_INTEGRATION_RCLONE]
    assert hass.data[DOMAIN_INTEGRATION_RCLONE][config_entry.entry_id].master

async def test_unload_entry(
    hass: HomeAssistant, entry: ConfigEntry
) -> None:
    """Test being able to unload an entry."""
    config_entry = await async_setup_entry(hass, entry)
    assert hass.data[DOMAIN_INTEGRATION_RCLONE]

    assert await async_unload_entry(hass, config_entry)
    assert not hass.data[DOMAIN_INTEGRATION_RCLONE]
