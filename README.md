# o2 HomeBox 6641 presence detection for Home Assistant

Tested o2 HomeBox 6641 firmware versions:
* 1.00(AAJG.0)D25b

## Configuration
The O2 HomeBox 6641 is slow to respond. Home Assistant querys device_trackers every 12s [by default](https://www.home-assistant.io/integrations/device_tracker/#configuring-a-device_tracker-platform). Increase the interval to a value the O2 HomeBox 6641 can handle, e.g. 30s.

In configuration.yaml:
```
device_tracker:
  platform: o2homebox6641
  interval_seconds: 30
```


## Known limitations
* Does not support password protection; authentication is yet to be implemented.
* O2 HomeBox 6641 does not support HTTPS, i.e. all traffic is in plain text. This would include authentication if authentication were implemented.
* Some devices do not provide a proper host name as part of their dhcp request to the o2 HomeBox, e.g. certain Android phones. These devices will not be reported. Try setting the host name in the Android Developer Options.
* Occasionally, the device overview provided by the O2 HomeBox 6641 may not show any connected wifi devices (maybe if it's low on memory?). This component will gracefully skip invalid data sets. This should not be a problem since Home Assistant will query the status periodically.

Based on Home Assistant's [swisscom](https://github.com/home-assistant/core/tree/dev/homeassistant/components/swisscom) integration.
