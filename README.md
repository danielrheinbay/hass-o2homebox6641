# o2 HomeBox 6641 presence detection for Home Assistant

Tested o2 HomeBox 6641 firmware versions:
* 1.00(AAJG.0)D25b

## Known limitations
* Does not support password protection; authentication is yet to be implemented.
* Some devices do not provide a proper host name as part of their dhcp request to the o2 HomeBox, e.g. certain Android phones. Try setting the host name in the Android Developer Options.
* Occasionally, the device overview provided by the O2 HomeBox 6641 may not show any connected wifi devices. Try rebooting the HomeBox.

Based on Home Assistant's [swisscom integration](https://github.com/home-assistant/core/tree/dev/homeassistant/components/swisscom) integration.