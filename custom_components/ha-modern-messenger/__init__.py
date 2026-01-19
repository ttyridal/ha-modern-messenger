import logging
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.httpx_client import get_async_client
from homeassistant.components.persistent_notification import (
    async_create,
)  # Import helper
from .const import DOMAIN, APPNAME
from . import api

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.SENSOR]


async def ha_notify_and_log(hass, txt):
    _LOGGER.error("%s", err)
    async_create(
        hass,
        message=txt,
        title="%s Error" % APPNAME,
        notification_id=f"facebook_error_123",  # ID keeps it unique per target
    )


async def send_notification(hass: HomeAssistant, entry: ConfigEntry, call: ServiceCall):
    token = entry.data.get("access_token")
    if not token:
        ha_notify_and_log(hass, "Invalid configuration, missing token")
        return
    aliases = dict([x.split("=", 2) for x in entry.data.get("aliases", [])])
    message = call.data.get("message")
    targets = call.data.get("targets", [])
    mapped_targets = [aliases.get(t, t) for t in targets]
    _LOGGER.info(
        "Posting to %s",
        ",".join(f"{alias}{handle}" for alias, handle in zip(targets, mapped_targets)),
    )
    image_entity_id = call.data.get("image_entity")
    image_url = call.data.get("image_url")
    image_bytes = None

    if image_entity_id:
        component = hass.data.get("image")
        if component and (entity := component.get_entity(image_entity_id)):
            try:
                image_bytes = await entity.async_image()
            except Exception as e:
                _LOGGER.error("Image fetch failed: %s", e)
    elif image_url:
        async_client = get_async_client(hass)
        try:
            response = await async_client.get(image_url, timeout=10)
            response.raise_for_status()
            image_bytes = response.content
        except Exception as e:
            _LOGGER.error("Failed to download image from URL %s: %s", image_url, e)

    successful_sends = 0
    try:
        successful_sends = await api.send_message(
            get_async_client(hass), message, image_bytes, mapped_targets, token
        )
    except api.GenericError as err:
        ha_notify_and_log(hass, "%s failed apicall: %s" % (APPNAME, err))

    sensor = hass.data[DOMAIN][entry.entry_id].get("sensor")
    if sensor:
        sensor.increment(successful_sends)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # Initialize data storage for this entry
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def handle_send_notification(call: ServiceCall):
        await send_notification(hass, entry, call)

    hass.services.async_register(DOMAIN, "send_notification", handle_send_notification)
    return True
