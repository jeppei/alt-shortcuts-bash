#!/usr/bin/env python3
import os
import subprocess
import bashcommands


def add_shortcut(name, command, binding):
    print("Adding shortcut"
          ": name=" + name +
          ", command=" + command +
          ", binding=" + binding)

    # defining keys & strings to be used
    key = "org.gnome.settings-daemon.plugins.media-keys custom-keybindings"
    subkey1 = key.replace(" ", ".")[:-1]+":"
    item_s = "/"+key.replace(" ", "/").replace(".", "/")+"/"
    firstname = "custom"
    # get the current list of custom shortcuts
    get = lambda cmd: subprocess.check_output(["/bin/bash", "-c", cmd]).decode("utf-8")
    array_str = get("gsettings get "+key)
    # in case the array was empty, remove the annotation hints
    command_result = array_str.lstrip("@as")
    current = eval(command_result)
    # make sure the additional keybinding mention is no duplicate
    n = 1
    while True:
        new = item_s+firstname+str(n)+"/"
        if new in current:
            n = n+1
        else:
            break
    # add the new keybinding to the list
    current.append(new)
    # create the shortcut, set the name, command and shortcut key
    cmd0 = 'gsettings set '+key+' "'+str(current)+'"'
    cmd1 = 'gsettings set '+subkey1+new+" name '"+name+"'"
    cmd2 = 'gsettings set '+subkey1+new+" command '"+command+"'"
    cmd3 = 'gsettings set '+subkey1+new+" binding '"+binding+"'"

    for cmd in [cmd0, cmd1, cmd2, cmd3]:
        subprocess.call(["/bin/bash", "-c", cmd])


# Remove all current shortcuts
bashcommands.BashCommands.execute_bash_command('gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "[]"')


parent = os.path.dirname(os.path.abspath(__file__))
altKey = "<Alt>"
for letter_index in range(ord('a'), ord('z')+1):
    letter = chr(letter_index)
    add_shortcut(
        f"altshortcut {letter}",
        f"python3 {parent}/../python/main.py {letter}",
        f"{altKey}{letter}"
    )


add_shortcut("Left click on §", "xdotool click --delay 5000 --repeat 1 1", "section")
add_shortcut("Right click on shift+§", "xdotool key shift+F10", "<shift>section")
add_shortcut("flameshot", "flameshot gui", "<Ctrl><Alt>s")
add_shortcut("Äxit", "gnome-session-quit --power-off", "<Alt>adiaeresis")
add_shortcut("Minimize window", "xdotool windowminimize $(xdotool getactivewindow)", "<Super>down")
