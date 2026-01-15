# Modern Messenger
[![hacs_badge](https://img.shields.io)](https://github.com)
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ttyridal&repository=ha-modern-messenger&category=Notify+integration)

This integration provides a notification target for Facebook Messenger. It is a modern alternative to the 
legacy integration, fully configurable from the UI. It supports sending text, url to images and entity.image.

## Prerequisites
*   You still need a facebook page and app as described in [integrations/facebook](https://www.home-assistant.io/integrations/facebook/)
*   A working installation of the [Home Assistant Community Store (HACS)](https://hacs.xyz/) in your Home Assistant instance.

---

## Installation

The preferred method is to install **Modern Messenger** via HACS.

### HACS (Recommended)

1.  **Open HACS** in your Home Assistant frontend.
2.  Navigate to **Integrations**.
3.  Click the **`+ EXPLORE & DOWNLOAD REPOSITORIES`** button in the bottom-right corner.
4.  **Search** for `Modern Messenger` and select the repository.
5.  Click **Download** and select the desired version (latest is recommended).
6.  **Restart** Home Assistant when prompted to ensure the new integration is loaded.

### Manual Installation (Advanced Users Only)

1.  Navigate to your Home Assistant configuration directory (`config/`).
2.  If it doesn't exist, create a `custom_components` directory.
3.  Inside `custom_components`, create a new folder named `modern_messenger`.
4.  Download all files from the `custom_components/modern_messenger/` directory in this GitHub repository and place them in the new folder you created.
5.  **Restart** Home Assistant.

---

## Configuration

Once the integration is installed and Home Assistant restarted, you can configure it via the UI:

1.  Go to **Settings** > **Devices & Services**.
2.  Click the **`+ ADD INTEGRATION`** button in the bottom-right corner.
3.  **Search** for `Modern Messenger` and select it.
4.  Follow the prompts in the configuration flow to enter any required information (e.g., API keys, user IDs).
5.  The integration should now be set up and ready to use.

---

## Usage

You use the integration by setting up automations with modern_messenger as the service.

```yaml
# Example automation
automation:
  - alias: "Send a message when door opens"
    trigger:
      platform: state
      entity_id: binary_sensor.door_contact
      to: 'on'
    action:
      - service: notify.modern_messenger
        data:
          message: "The front door just opened!"
          target: "me" 

