#!/bin/bash

# Remove all custom shortcuts
gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "[]"

# Add custom shortcuts
altKey="<Alt>"
# altKey="<Super>"
dir="$(pwd)"
parent="$(dirname "$dir")"
for letter in {a..x}
do
    if [[ "$x" != "l" ]]; then # used for locking the screen
        python3 add-shortcut.py "altshortcut $letter" "python3 $parent/alt-shortcuts-python/main.py $letter" "$altKey$letter"
    fi
done
python3 add-shortcut.py "altshortcut 1" "python3 $parent/alt-shortcuts-python/main.py 1" $altKey"1"
python3 add-shortcut.py "Left click on §" "xdotool click --delay 5000 --repeat 1 1" "section"
python3 add-shortcut.py "Right click on shift+§" "xdotool key shift+F10" "<shift>section"
python3 add-shortcut.py "flameshot" "flameshot gui" "<Ctrl><Alt>s"
python3 add-shortcut.py "Äxit" "gnome-session-quit --power-off" "<Alt>adiaeresis"
python3 add-shortcut.py "Minimize window" "xdotool windowminimize $(xdotool getactivewindow)" "<Super>down"