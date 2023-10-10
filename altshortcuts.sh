#!/bin/bash
# Location of some apps
# /usr/bin
# /snap/bin
# use "which <application>" to determine where it is installed"
# You can also check the process with "ps aux | grep <application>" and then "/proc/<process-id>/exe

printf "
    █████╗ ██╗  ████████╗    ███████╗██╗  ██╗ ██████╗ ██████╗ ████████╗ ██████╗██╗   ██╗████████╗███████╗
   ██╔══██╗██║  ╚══██╔══╝    ██╔════╝██║  ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██║   ██║╚══██╔══╝██╔════╝
   ███████║██║     ██║       ███████╗███████║██║   ██║██████╔╝   ██║   ██║     ██║   ██║   ██║   ███████╗
   ██╔══██║██║     ██║       ╚════██║██╔══██║██║   ██║██╔══██╗   ██║   ██║     ██║   ██║   ██║   ╚════██║
   ██║  ██║███████╗██║       ███████║██║  ██║╚██████╔╝██║  ██║   ██║   ╚██████╗╚██████╔╝   ██║   ███████║
   ╚═╝  ╚═╝╚══════╝╚═╝       ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝
\n\n"

function AskUserForSuggestions() {
	# Get suggestions from app.txt, starting with $letter, but not the current app
	suggestions=$(awk -v s="$letter" 'index($0, s) == 1' $path | awk 'BEGIN {FS="#"} {print $1}'| sed '/'$currentProcessName'/d')
	askToLaunch=$(awk -v s="$letter" 'index($0, s) == 1' $path | awk 'BEGIN {FS="#"} {print $3}')
	printf "\n#### No (other) active windows matches the letter. Here are some suggestions\n$suggestions\n"
	[ -z "$suggestions" ] && printf "No suggestions found. Will exit.\n" && exit 0

	# shellcheck disable=SC2086
	noSuggestions="$(echo $suggestions | wc -w)"
	echo "ask to alunch "$askToLaunch
	if [[ $noSuggestions == 1 && $askToLaunch -eq 0 ]]; then
	  ans=$suggestions
	else
	  ans=$(zenity --list --column=Apps --height 300 $suggestions)
	fi
	printf "\n#### You picked: $ans\n"

	[ -z "$ans" ] && printf "\nReceived no user input. Will exit\n" && exit 0

	command="$(grep "^$ans" "$path" | awk 'BEGIN {FS="#"} {print $4}')"
	$command
	printf "\n###Command $command executed will exit now\n"; exit 0
}

function ActivateTheOnlyWindows() {
  mathedTranslatedWindowsFixedIds=$2

	printf "\n#### There is more than one match! Will try to find the most recent one.\n"
	# Find the most recent window starting on the letter
	for ((i=${#processStack[@]}-1; i>=0; i--)); do
	  process="${processStack[$i]}"
	  for match in ${mathedTranslatedWindowsFixedIds}; do

      printf "Will process [$process] match with [$match]"
      if [[ "$process" == "$match" ]]; then
        printf " --> Match! \n"
        realMatch=${match//0x/0x0}
        printf "Will switch to window with process id $realMatch"
        wmctrl -ia $realMatch
        printf "\n###Switched window to $realMatch. Will exit now\n"; exit 0
      fi
      printf " --> No match!\n"
	  done
	done
	printf "\nError: Could not find a matching process\n"
}

function TryFindAnotherWindowToActivate() {

  printf "\n#### Current window is a match. Will see if I can find another one to change to.\n"
  printf "\nprocessStack: $processStack\n"
	# Go backwards in the processStack to find another windows starting on the same letter
	for win in ${processStack}; do
		for match in ${matchedFixedIds}; do
			if [[ "$win" == "$match" ]]; then
				realMatch=${match//0x/0x0}

				if [[ "$match" == "$currentProcessId" ]]; then
          printf "No match found\n"
					# Get suggestions from app.txt, starting with $letter, but not the current app
          AskUserForSuggestions $1
				fi

				wmctrl -ia $realMatch
				printf "\n###EXIT 06\n"
				exit 0
			fi
		done
	done

}

function ActivateOldestWindowsOnLetter() {
  printf "\n#### There is more than one match! Will try to find the most recent one.\n"
  # Find the most recent window starting on the letter
	processes=($processStack)
	for ((i=${#processes[@]}-1; i>=0; i--)); do
	  process="${processes[$i]}"
	  for match in ${matchedFixedIds}; do

      printf "Will process [$process] match with [$match]"
      if [[ "$process" == "$match" ]]; then
        printf " --> Match! \n"
        realMatch=${match//0x/0x0}
        printf "Will switch to window with process id $realMatch"
        wmctrl -ia $realMatch
        printf "\n###EXIT 06\n"
        exit 0
      fi
      printf " --> No match!\n"
	  done
	done
	printf "\nError: Could not find a matching process\n"
}

function FixProcessIds() {
  # Some processes (like chrome) have mulitple 0 after '0x' in the process id while the process
  # processStack always have no 0 after the '0x' in the process id. Hence we try to remove them twice.
  echo "$matchedIds" | sed "s/0x0/0x/" | sed "s/0x0/0x/"
}

PrintVariables() {
  ## Print variables
  printf "Letter: "$letter"\n"
  printf "Apps.txt path: $path\n"
  printf "\n#### windows\n"
  printf "$windows\n"
  printf "\n#### windowsTranslated\n"
  printf "$windowsTranslated\n"
  printf "\nCurrent process id: $currentProcessId\n"
  printf "Current process name: $currentProcessName\n"
  if [ -z "$mathedTranslatedWindows" ]; then
    printf "\n<<<No matches on \"$letter\">>>\n";
  else
    printf "\n#### mathedTranslatedWindows\n"
    printf "$mathedTranslatedWindows\n"
    printf "\n#### matchedIds\n"
    printf "$matchedIds\n"
    printf "\n#### matchedFixedIds\n"
    printf "$matchedFixedIds\n"
  fi
}

function TranslateWindows() {
  windowsTranslated="$(wmctrl -xl | grep -v gjs.Gjs | awk '{ print $3" "$1}')"
  while read -r p; do
    from="$(echo $p | awk 'BEGIN {FS="#"} {print $2}' | xargs)"
    to="$(echo $p | awk 'BEGIN {FS="#"} {print $1}' | xargs)"

    if [ "$from" != "" ]; then
      windowsTranslated="${windowsTranslated//$from/$to}"
    fi
  done <$path
  printf "$windowsTranslated\n"
}

######################################################
##            ACTUAL CODE STARTS HERE               ##
######################################################

# Close existing zenity windows (the ones the suggest different applications)
wmctrl -lix |grep 'zenity.Zenity' | cut -d ' ' -f 1 | xargs -i% wmctrl -i -c %

letter=$1
path="$( dirname -- "$0"; )/apps.txt"; # Full path to apps.txt
windows="$(wmctrl -xl | grep -v gjs.Gjs | awk '{ print $3" "$letter}')"  # Not sure what gjs is but this should be in a file with ignores
windowsTranslated="$(TranslateWindows $windows)"
mathedTranslatedWindows="$(echo "$windowsTranslated" | grep "^$letter")"
matchedIds="$(echo "$mathedTranslatedWindows" | awk '{print $2}')"
matchedFixedIds="$(FixProcessIds)"
processStack="$(xprop -root | grep "^_NET_CLIENT_LIST_STACKING" | cut -c 48- | tr ", " " ")"
currentProcessId=${processStack##* }
currentProcessName=$(echo "$windowsTranslated" | sed "s/0x0/0x/" | grep "$currentProcessId" | awk '{print $1}')
source /home/jesper/.profile

PrintVariables

if [ -z "$mathedTranslatedWindows" ]; then # No windows matches letter
  AskUserForSuggestions $1

elif [[ "$matchedFixedIds" == *"$currentProcessId"* ]]; then # Current window matches letter
  TryFindAnotherWindowToActivate $1

else # There is a window matching the letter and its not the current one
  ActivateOldestWindowsOnLetter $1

fi
printf "Error: The altShortcuts should never end up here. Something is wrong....\n"
