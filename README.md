## Wallpaper Changer

`wallpaper_changer` is a Python package that sets the desktop wallpaper on Linux. It supports the desktop environments listed below.

### Installation

Install `wallpaper_changer` with pip:

```bash
pip install wallpaper_changer
```

### Usage

Call `set_wallpaper` with a local file path or a URL:

```python
import wallpaper_changer

# Set wallpaper from a local file
wallpaper_changer.set_wallpaper('/path/to/your/image.jpg')

# Set wallpaper from a URL
wallpaper_changer.set_wallpaper('https://example.com/your/image.jpg')
```

If you do not pass `desktop_env`, the package detects the current desktop environment from the session environment variables.

### Supported Desktop Environments

- **GNOME**: `gnome`, `unity`, `cinnamon`
- **MATE**: `mate`
- **XFCE**: `xfce4`
- **KDE**: `kde`
- **LXDE**: `lxde`
- **Fluxbox**: `fluxbox`
- **Openbox**: `openbox`
- **IceWM**: `icewm`
- **JWM**: `jwm`
- **AfterStep**: `afterstep`
- **Blackbox**: `blackbox`
- **WindowMaker**: `windowmaker`

### Notes

Some desktop environments need extra dependencies. GNOME-based environments need `pygobject`. KDE needs `dbus-python`. Install the dependency for your desktop environment before you call `set_wallpaper`.

### Compatibility

This package targets Linux. It does not work on Windows or macOS, because those systems use different desktop management APIs.

### Related Projects

- [OpenVoiceOS/ovos-PHAL-plugin-wallpaper-manager](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-wallpaper-manager), a PHAL plugin for OpenVoiceOS devices. It coordinates wallpaper providers and calls `wallpaper_changer.set_wallpaper` to apply the desktop wallpaper.

### Issues and Contributions

If you find an issue or have a suggestion, open an issue or submit a pull request.
