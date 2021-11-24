"""Support for o2 HomeBox 6641 routers."""
import logging
import requests
import voluptuous as vol
import pandas as pd

from homeassistant.components.device_tracker import (
    DOMAIN,
    PLATFORM_SCHEMA as PARENT_PLATFORM_SCHEMA,
    DeviceScanner,
)
from homeassistant.const import CONF_HOST
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_IP = "o2.box"

PLATFORM_SCHEMA = PARENT_PLATFORM_SCHEMA.extend(
    {vol.Optional(CONF_HOST, default=DEFAULT_IP): cv.string}
)


def get_scanner(hass, config):
    """Return the o2HomeBox6641 device scanner."""
    scanner = o2HomeBox6641DeviceScanner(config[DOMAIN])

    return scanner if scanner.success_init else None


class o2HomeBox6641DeviceScanner(DeviceScanner):
    """This class queries a router running o2HomeBox6641 Internet-Box firmware."""

    def __init__(self, config):
        """Initialize the scanner."""
        self.host = config[CONF_HOST]
        self.last_results = {}

        # Test the router is accessible.
        data = self.get_o2HomeBox6641_data()
        self.success_init = data is not None

    def scan_devices(self):
        """Scan for new devices and return a list with found device IDs."""
        self._update_info()
        return list(self.last_results.keys())

    def get_device_name(self, device):
        """Return the name of the given device or None if we don't know."""
        if not self.last_results:
            return None
        return self.last_results.get(device)

    def _update_info(self):
        """Ensure the information from the o2 HomeBox 6641 router is up to date.

        Return boolean if scanning successful.
        """
        if not self.success_init:
            return False

        _LOGGER.info("Loading data from o2 HomeBox 6641.")
        if not (data := self.get_o2HomeBox6641_data()):
            return False

        self.last_results = data
        return True

    def get_o2HomeBox6641_data(self):
        """Retrieve data from o2 HomeBox 6641 and return parsed result."""
        url_device_mac_addresses = f"http://{self.host}/scmacflt.cmd?action=view"

        try:
            request_mac_addresses = requests.get(url_device_mac_addresses)
            request_mac_addresses.encoding = "utf-8"
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectTimeout,
        ):
            _LOGGER.error("No response from o2 HomeBox 6641.")
            return None
        
        html_mac_addresses = request_mac_addresses.content
        df_mac_addresses = pd.read_html(html_mac_addresses, header=0, index_col=2, encoding="utf-8")[1].head(-2)
        df_mac_addresses.drop(df_mac_addresses.columns[:2], axis=1, inplace=True)
        dictionary = df_mac_addresses.to_dict()

        return dictionary.get("Host-Name")
