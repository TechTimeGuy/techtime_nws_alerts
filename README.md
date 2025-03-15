🛰️ Techtime NWS Alerts for Home Assistant

Techtime NWS Alerts is a custom integration for Home Assistant that provides real-time weather alerts from the National Weather Service (NWS) directly into your smart home dashboard. Stay informed of critical weather events and automate actions based on the latest alerts!
🚀 Features

✅ Real-time NWS alerts
✅ Displays event type, headline, severity, urgency, and more
✅ Works with Home Assistant automations and notifications
✅ Easy to install and configure through the Home Assistant UI
✅ Supports multiple zone configurations
✅ Asynchronous fetching for lightweight and efficient performance
✅ Updates every 5 minutes
✅ Clean and simple Lovelace cards
✅ Open-source and actively maintained
📦 Installation
Manual Installation (Custom Components Folder)

    Download the latest release from the GitHub repository.
    Or clone directly:

git clone https://github.com/TechTimeGuy/techtime_nws_alerts.git

Copy the techtime_nws_alerts folder into your Home Assistant custom_components directory:

/config/custom_components/techtime_nws_alerts/

The structure should look like:

    custom_components/
      techtime_nws_alerts/
        __init__.py
        sensor.py
        config_flow.py
        const.py
        manifest.json
        translations/en.json

    Restart Home Assistant.

⚙️ Configuration
UI Setup (Recommended)

    Go to Home Assistant → Settings → Devices & Services → Integrations.
    Click + Add Integration and search for Techtime NWS Alerts.
    Enter your NWS Zone ID (e.g., NCC019) and click Submit.
    The sensor will be created automatically.

🔗 Find your NWS Zone ID:

👉 https://www.weather.gov/gis/Zone
Example: NCC019 (Brunswick County, NC)
🖥️ Lovelace Dashboard Examples
Basic Entity Card

type: entity
entity: sensor.techtime_nws_alerts
name: Techtime NWS Alerts
icon: mdi:alert

Entities Card with Attributes

type: entities
title: NWS Weather Alerts
entities:
  - entity: sensor.techtime_nws_alerts
    name: Alert Status
  - entity: sensor.techtime_nws_alerts
    attribute: headline
    name: Headline
  - entity: sensor.techtime_nws_alerts
    attribute: description
    name: Description
  - entity: sensor.techtime_nws_alerts
    attribute: severity
    name: Severity
  - entity: sensor.techtime_nws_alerts
    attribute: urgency
    name: Urgency
  - entity: sensor.techtime_nws_alerts
    attribute: instruction
    name: Instructions

🔔 Example Automation

Trigger notifications or actions when a new alert is issued:

alias: Notify on New NWS Alert
trigger:
  - platform: state
    entity_id: sensor.techtime_nws_alerts
    from: "No Alerts"
condition: []
action:
  - service: notify.notify
    data:
      message: |
        🚨 New NWS Alert:
        {{ state_attr('sensor.techtime_nws_alerts', 'headline') }}

        {{ state_attr('sensor.techtime_nws_alerts', 'description') }}

📋 Sensor Attributes
Attribute	Description
headline	Short summary of the alert event
description	Full description of the alert
effective	When the alert becomes effective
expires	When the alert expires
instruction	Specific instructions to follow
severity	Severity level (Minor, Moderate, Severe, etc.)
certainty	Certainty level (Likely, Possible, Observed, etc.)
urgency	Urgency level (Expected, Immediate, Future, etc.)
🛠️ Troubleshooting

    Ensure you have the correct zone_id during setup.
    Check Settings → Logs in Home Assistant for errors.
    Verify the NWS API is available by visiting https://api.weather.gov.

✅ To-Do / Planned Features

Configurable update interval
Multi-zone support in a single sensor
HACS support for easy installation

    More languages (translations)

❤️ Credits

    Data provided by NOAA / NWS Weather API
    Developed by @TechTimeGuy

📄 License

MIT License
Feel free to share, fork, and contribute!
🔗 GitHub Repo

👉 https://github.com/TechTimeGuy/techtime_nws_alerts