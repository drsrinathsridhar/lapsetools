# This script renames some files to avoid the *** Error (-60: 'Could not lock the device') *** for the Nikon D40x
# See https://www.raspberrypi.org/forums/viewtopic.php?t=70049
#!/bin/bash
sudo mv /usr/share/dbus-1/services/org.gtk.Private.GPhoto2VolumeMonitor.service /usr/share/dbus-1/services/org.gtk.Private.GPhoto2VolumeMonitor.service.bkp
sudo mv /usr/share/gvfs/mounts/gphoto2.mount /usr/share/gvfs/mounts/gphoto2.mount.bkp
sudo mv /usr/share/gvfs/remote-volume-monitors/gphoto2.monitor /usr/share/gvfs/remote-volume-monitors/gphoto2.monitor.bkp
sudo mv /usr/lib/gvfs/gvfs-gphoto2-volume-monitor /usr/lib/gvfs/gvfs-gphoto2-volume-monitor.bkp