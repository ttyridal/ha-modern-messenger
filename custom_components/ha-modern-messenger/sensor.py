from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import EntityCategory
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, APPNAME


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    # We store the sensor object in hass.data so the service can find it
    sensor = FacebookDiagnosticSensor(entry)
    hass.data[DOMAIN][entry.entry_id]["sensor"] = sensor
    async_add_entities([sensor])


class FacebookDiagnosticSensor(SensorEntity):
    """Diagnostic sensor to count notifications."""

    _attr_name = "Notifications Sent"
    _attr_native_value = 0
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_icon = "mdi:facebook-messenger"

    def __init__(self, entry):
        self._attr_unique_id = f"{entry.entry_id}_sent_count"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=APPNAME,
        )

    def increment(self, count=1):
        """Increment the internal counter."""
        self._attr_native_value += count
        self.async_write_ha_state()
