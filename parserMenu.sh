#!/usr/bin/bash

mainMenu() {
cyanPrint "=========== THE ULTIMATE PP2000 ============"

printf "$(greenPrint '1)') Run prelim\n"
printf "$(greenPrint '2)') Logs\n"
printf "$(greenPrint '3)') Troubleshooting\n"
printf "$(greenPrint '4)') Set time\n"
printf "$(redPrint '0)') Exit\n"
printf "Choose an option: "
	read -r ans
	case $ans in
		1)
			prelimMenu
			;;
		2)
			logMenu
			;;
		3)
			troubleshootingMenu
			;;
		4)
			setTime
			;;
		0)
			printf 'Bye bye.\n'
			exit 0
			;;
		*)
			printf 'Wrong option.\n'
			mainMenu
			;;
	esac
}

logMenu() {
	printf '
========= LOG MENU =========

1) Collect and merge logs
2) Clear bad logs
3) Go back to main menu
0) Exit
Choose an option:  '
	read -r ans
	case $ans in
		1)
			printf 'Collecting logs\n'
			logMenu
			;;
		2)
			printf 'Clear bad logs\n'
			logMenu
			;;
		3)
			mainMenu
			;;
		0)
			printf "Bye bye.\n"
			exit 0
			;;
		*)
			printf "Wrong option.\n"
			logMenu
			;;

	esac
}

prelimMenu() {
	printf '
========= PRELIM MENU =========

Select a model to run

1) Run BGW210
2) Ping RG
3) Go Back to Main Menu
0) Exit
Choose an option:  '
	read -r ans
	case $ans in
		1)
			printf 'Running BGW210 Parser\n'
			prelimMenu
			;;
		2)
			printf 'Pinging RG\n'
			prelimMenu
			;;
		3)
			mainMenu
			;;
		0)
			printf "Bye bye.\n"
			exit 0
			;;
		*)
			printf "Wrong option."
			prelimMenu
			;;
	esac
}

troubleshootingMenu() {
	printf '
============ TROUBLESHOOTING ===============

What do you have problems with?

1) Index out of range
2) Cannot set time
3) Error exit code 255
0) Exit
Choose an option:  '
	read -r ans
	case $ans in
		1)
			printf 'Something is wrong with wifi page.\n'
			troubleshootingMenu
			;;
		2)
			printf 'Make sure you can ssh into client pcs.\n'
			troubleshootingMenu
			;;
		3)
			printf 'Units cannot connect to RG GUI or ssh protocol failed.\n'
			troubleshootingMenu
			;;
		0)
			printf 'Bye bye.\n'
			exit 0
			;;
		*)
			printf 'Wrong option.\n'
			troubleshootingMenu
			;;
	esac
}

setTime() {
	greenprint "Time is set."
	mainMenu
}
### Colors ##
ESC=$(printf '\033')
RESET="${ESC}[0m"
RED="${ESC}[31m"
GREEN="${ESC}[32m"
YELLOW="${ESC}[33m"
BLUE="${ESC}[34m"
MAGENTA="${ESC}[35m"
CYAN="${ESC}[36m"

### Color Functions ##
redPrint() { printf "${RED}%s${RESET}" "$1"; }
greenPrint() { printf "${GREEN}%s${RESET}" "$1"; }
yellowPrint() { printf "${YELLOW}%s${RESET}" "$1"; }
bluePrint() { printf "${BLUE}%s${RESET}" "$1"; }
magentaPrint() { printf "${MAGENTA}%s${RESET}" "$1"; }
cyanPrint() { printf "${CYAN}%s${RESET}\n" "$1"; }

mainMenu
