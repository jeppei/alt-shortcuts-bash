#!/bin/bash

# Remove all custom shortcuts
gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "[]"

# Add custom shortcuts
altKey="<Alt>"
# altKey="<Super>"
dir="$(pwd)"
parent="$(dirname "$dir")"
for x in {a..x}
do
    if [[ "$x" != "l" ]]; then # used for locking the screen
        python3 add-shortcut.py "altshortcut $x" "bash $parent/altshortcuts.sh $x" "$altKey$x"
    fi
done
python3 add-shortcut.py "altshortcut 1" "bash $parent/altshortcuts.sh 1" $altKey"1"
python3 add-shortcut.py "Leftclick on §" "xdotool click --delay 5000 --repeat 1 1" "section"
python3 add-shortcut.py "flameshot" "flameshot gui" "<Ctrl><Alt>s"
python3 add-shortcut.py "Äxit" "gnome-session-quit --power-off" "<Alt>adiaeresis"