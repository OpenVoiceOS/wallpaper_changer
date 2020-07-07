import os
import re
import requests
import sys
import subprocess
from os.path import join, expanduser


def set_wallpaper(file_loc, desktop_env=None):
    if file_loc.startswith("http"):
        r = requests.get(file_loc)
        file_loc = join(expanduser("~"), "wallpaper.jpg")
        if r.status_code == requests.codes.ok:
            with open(file_loc, 'wb') as f:
                f.write(r.content)
        else:
            print("ERROR downloading wallpaper")
            return False

    desktop_env = desktop_env or get_desktop_environment()
    desktop_env = desktop_env.lower()
    try:
        if desktop_env in ["gnome", "unity", "cinnamon"]:
            uri = "'file://%s'" % file_loc
            try:
                try:
                    from gi.repository import Gio
                except ImportError:
                    print("run pip install pygobject")
                    raise
                SCHEMA = "org.gnome.desktop.background"
                KEY = "picture-uri"
                gsettings = Gio.Settings.new(SCHEMA)
                gsettings.set_string(KEY, uri)
            except:
                args = ["gsettings", "set", "org.gnome.desktop.background",
                        "picture-uri", uri]
                subprocess.Popen(args)
        elif desktop_env == "mate":
            try:  # MATE >= 1.6
                # info from http://wiki.mate-desktop.org/docs:gsettings
                args = ["gsettings", "set", "org.mate.background",
                        "picture-filename", "'%s'" % file_loc]
                subprocess.Popen(args)
            except:  # MATE < 1.6
                # From https://bugs.launchpad.net/variety/+bug/1033918
                args = ["mateconftool-2", "-t", "string", "--set",
                        "/desktop/mate/background/picture_filename",
                        '"%s"' % file_loc]
                subprocess.Popen(args)
        elif desktop_env == "gnome2":  # Not tested
            # From https://bugs.launchpad.net/variety/+bug/1033918
            args = ["gconftool-2", "-t", "string", "--set",
                    "/desktop/gnome/background/picture_filename",
                    '"%s"' % file_loc]
            subprocess.Popen(args)
        ## KDE4 is difficult
        ## see http://blog.zx2c4.com/699 for a solution that might work
        elif desktop_env in ["kde3", "trinity"]:
            # From http://ubuntuforums.org/archive/index.php/t-803417.html
            args = 'dcop kdesktop KBackgroundIface setWallpaper 0 "%s" 6' % file_loc
            subprocess.Popen(args, shell=True)
        elif desktop_env in ["xfce4", "xfce"]:
            # From http://www.commandlinefu.com/commands/view/2055/change-wallpaper-for-xfce4-4.6.0
            # Not working in xubuntu, seems that prop name changed
            # try to auto detect correct prop name to use
            props = subprocess.check_output(["xfconf-query", "-lc",
                                             "xfce4-desktop"]) \
                .decode("utf-8").split("\n")
            props = [p for p in props if "last-image" in p or "image-path"
                     in p]
            for p in props:
                args = ["xfconf-query", "-c", "xfce4-desktop", "-p", p, "-s",
                        file_loc]
                subprocess.Popen(args)
            subprocess.Popen(["xfdesktop", "--reload"])
        elif desktop_env in ["fluxbox", "jwm", "openbox", "afterstep"]:
            # http://fluxbox-wiki.org/index.php/Howto_set_the_background
            # used fbsetbg on jwm too since I am too lazy to edit the XML configuration
            # now where fbsetbg does the job excellent anyway.
            # and I have not figured out how else it can be set on Openbox and AfterSTep
            # but fbsetbg works excellent here too.
            try:
                args = ["fbsetbg", file_loc]
                subprocess.Popen(args)
            except:
                print(
                    "ERROR: Failed to set wallpaper with fbsetbg!\n")
                print(
                    "Please make sre that You have fbsetbg installed.\n")
        elif desktop_env == "icewm":
            # command found at http://urukrama.wordpress.com/2007/12/05/desktop-backgrounds-in-window-managers/
            args = ["icewmbg", file_loc]
            subprocess.Popen(args)
        elif desktop_env == "blackbox":
            # command found at http://blackboxwm.sourceforge.net/BlackboxDocumentation/BlackboxBackground
            args = ["bsetbg", "-full", file_loc]
            subprocess.Popen(args)
        elif desktop_env == "lxde":
            args = "pcmanfm --set-wallpaper %s --wallpaper-mode=scaled" % file_loc
            subprocess.Popen(args, shell=True)
        elif desktop_env == "windowmaker":
            # From http://www.commandlinefu.com/commands/view/3857/set-wallpaper-on-windowmaker-in-one-line
            args = "wmsetbg -s -u %s" % file_loc
            subprocess.Popen(args, shell=True)
        elif desktop_env == "kde":
            try:
                import dbus
            except ImportError:
                print("pip install dbus-python")
                raise
            bus = dbus.SessionBus()
            remote_object = bus.get_object("org.kde.plasmashell",
                                           "/PlasmaShell")
            remote_object.evaluateScript(
                'var allDesktops = desktops();print (allDesktops);for ('
                'i=0;i<allDesktops.length;i++) {d = allDesktops['
                'i];d.wallpaperPlugin = "org.kde.image";d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");d.writeConfig("Image", "file://' + file_loc + '")}',
                dbus_interface="org.kde.PlasmaShell")
        else:
            return False
        return True
    except:
        print(
            "ERROR: Failed to set wallpaper.")
        return False


def get_desktop_environment():
    # From http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=1139057
    if sys.platform in ["win32", "cygwin"]:
        return "windows"
    elif sys.platform == "darwin":
        return "mac"
    else:  # Most likely either a POSIX system or something not much common

        def is_running(process):
            # From http://www.bloggerpolis.com/2011/05/how-to-check-if-a-process-is-running-using-python/
            # and http://richarddingwall.name/2009/06/18/windows-equivalents-of-ps-and-kill-commands/
            try:  # Linux/Unix
                s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
            except:  # Windows
                s = subprocess.Popen(["tasklist", "/v"],
                                     stdout=subprocess.PIPE)
            for x in s.stdout:
                if re.search(process, x):
                    return True
            return False

        desktop_session = os.environ.get("DESKTOP_SESSION") or \
                          os.environ.get("XDG_CURRENT_DESKTOP")
        if desktop_session is not None:
            # easier to match if we doesn't have  to deal with caracter cases
            desktop_session = desktop_session.lower()
            if desktop_session in ["gnome", "unity", "cinnamon", "mate",
                                   "xfce4", "lxde", "fluxbox",
                                   "blackbox", "openbox", "icewm", "jwm",
                                   "afterstep", "trinity", "kde"]:
                return desktop_session
            ## Special cases ##
            # Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
            # There is no guarantee that they will not do the same with the other desktop environments.
            elif "xfce" in desktop_session or desktop_session.startswith(
                    "xubuntu"):
                return "xfce4"
            elif desktop_session.startswith("ubuntu"):
                return "unity"
            elif desktop_session.startswith("lubuntu"):
                return "lxde"
            elif desktop_session.startswith("kubuntu"):
                return "kde"
            elif desktop_session.startswith("razor"):  # e.g. razorkwin
                return "razor-qt"
            elif desktop_session.startswith(
                    "wmaker"):  # e.g. wmaker-common
                return "windowmaker"

        if os.environ.get('KDE_FULL_SESSION') == 'true':
            return "kde"
        elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
            if not "deprecated" in os.environ.get(
                    'GNOME_DESKTOP_SESSION_ID'):
                return "gnome2"
        # From http://ubuntuforums.org/showthread.php?t=652320
        elif is_running("xfce-mcs-manage"):
            return "xfce4"
        elif is_running("ksmserver"):
            return "kde"
    return "unknown"
