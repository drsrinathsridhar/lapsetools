# This script resets the system to the old state. See setDaemonState.sh
# See https://www.raspberrypi.org/forums/viewtopic.php?t=70049
#!/bin/bash
sudo mv /usr/share/dbus-1/services/org.gtk.Private.GPhoto2VolumeMonitor.service.bkp /usr/share/dbus-1/services/org.gtk.Private.GPhoto2VolumeMonitor.service
sudo mv /usr/share/gvfs/mounts/gphoto2.mount.bkp /usr/share/gvfs/mounts/gphoto2.mount
sudo mv /usr/share/gvfs/remote-volume-monitors/gphoto2.monitor.bkp /usr/share/gvfs/remote-volume-monitors/gphoto2.monitor
sudo mv /usr/lib/gvfs/gvfs-gphoto2-volume-monitor.bkp /usr/lib/gvfs/gvfs-gphoto2-volume-monitor