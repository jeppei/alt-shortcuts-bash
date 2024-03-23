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
    if [[ "$letter" != "i" ]] && [[ "$letter" != "j" ]] && [[ "$letter" != "k" ]] && [[ "$letter" != "l" ]]; then # arrow keys
        python3 add-shortcut.py "altshortcut $letter" "python3 $parent/python/main.py $letter" "$altKey$letter"
    fi
done

python3 add-shortcut.py "Left click on §" "xdotool click --delay 5000 --repeat 1 1" "section"
python3 add-shortcut.py "Right click on shift+§" "xdotool key shift+F10" "<shift>section"

python3 add-shortcut.py "flameshot" "flameshot gui" "<Ctrl><Alt>s"
python3 add-shortcut.py "Äxit" "gnome-session-quit --power-off" "<Alt>adiaeresis"
python3 add-shortcut.py "Minimize window" "xdotool windowminimize $(xdotool getactivewindow)" "<Super>down"

#python3 add-shortcut.py "Up key" "xdotool key --clearmodifiers Up" $altKey"<Up>"
#python3 add-shortcut.py "Left key" "xdotool key --clearmodifiers Left" $altKey"<Left>"
#ython3 add-shortcut.py "Down key" "xdotool key --clearmodifiers Down" $altKey"<Down>"
#python3 add-shortcut.py "Right key" "xdotool key --clearmodifiers Right" $altKey"<Right>"