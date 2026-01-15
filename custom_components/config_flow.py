import voluptuous as vol
from homeassistant.helpers import selector
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, APPNAME

MAX_ALIASES = 5


def get_alias_schema(current_list=None):
    """Generate a schema with 5 alias fields."""
    current_list = current_list or ["me=1234"]
    schema = {}

    for i in range(MAX_ALIASES):
        # Pre-fill with existing data if available
        existing_val = current_list[i] if i < len(current_list) else ""
        schema[vol.Optional(f"alias_{i}", default=existing_val)] = (
            selector.TextSelector()
        )

    return vol.Schema(schema)


def parse_alias_input(user_input):
    """Filter out empty fields and return a clean list of strings."""
    return [
        user_input[f"alias_{i}"]
        for i in range(MAX_ALIASES)
        if user_input.get(f"alias_{i}") and user_input[f"alias_{i}"].strip()
    ]


class ModernFacebookConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self.access_token = None

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step."""
        errors = {}
        unique_id = "single_instance_integration_id"
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        """Step 1: Collect Access Token."""
        if user_input is not None:
            self.access_token = user_input["access_token"]
            return await self.async_step_aliases()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("access_token"): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        )
                    )
                }
            ),
            errors=errors,
        )

    async def async_step_aliases(self, user_input=None):
        """Step 2: Collect up to 5 Aliases."""
        errors = {}
        if user_input is not None:
            aliases = parse_alias_input(user_input)
            return self.async_create_entry(
                title=APPNAME,
                data={"access_token": self.access_token, "aliases": aliases},
            )

        return self.async_show_form(
            step_id="aliases", data_schema=get_alias_schema(), errors=errors
        )

    @staticmethod
    def async_get_options_flow(entry):
        return AliasOptionsFlowHandler(entry)


class AliasOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, entry):
        self.entry = entry

    async def async_step_init(self, user_input=None):
        errors = {}

        if user_input is not None:
            aliases = parse_alias_input(user_input)
            # This updates entry.options
            return self.async_create_entry(title="", data={"aliases": aliases})

        # Load current aliases from either data or options
        current_aliases = self.entry.options.get(
            "aliases", self.entry.data.get("aliases", [])
        )

        return self.async_show_form(
            step_id="init", data_schema=get_alias_schema(current_aliases), errors=errors
        )
