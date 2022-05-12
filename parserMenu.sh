#!/bin/bash

DESKTOP_PATH="/home/odroid/Desktop"
OUTPUT_PATH="$DESKTOP_PATH/Output"
ARCHIVE_PATH="$DESKTOP_PATH/Archive"
MERGE_PATH="$DESKTOP_PATH/merge"
PC1_ADDRESS="odroid@192.168.2.1"

mainMenu() {
printf "\n"
cyanPrintln "=========== THE ULTIMATE PP2000 ============"

printf "\n"
printf "$(greenPrint '1)') Run prelim\n"
printf "$(greenPrint '2)') Logs\n"
printf "$(greenPrint '3)') Troubleshooting\n"
printf "$(greenPrint '4)') Set time\n"
printf "$(redPrint '0)') Exit\n"
printf "\n"
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
printf "\n"
greenPrintln "========= LOG MENU ========="

printf "\n"
printf "$(cyanPrint '1)') Collect and merge logs\n"
printf "$(cyanPrint '2)') Clear bad logs\n"
printf "$(cyanPrint '3)') Go back to main menu\n"
printf "$(redPrint '0)') Exit\n"
printf "\n"
printf "Choose an option:  "
	read -r ans
	case $ans in
		1)
            ~/Desktop/collect.sh
			logMenu
			;;
		2)
			printf 'Clear bad logs\n'
            # Delete all Output files on remote clients
            parallel-ssh -h clients.txt "rm $OUTPUT_PATH/*.csv"
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
printf "\n"
cyanPrintln "========= PRELIM MENU ========="

printf "\nSelect a model to run\n"
printf "\n"
printf "$(greenPrint '1)') Run BGW210\n"
printf "$(greenPrint '2)') Run BGW320\n"
printf "$(greenPrint '3)') Ping RG @192.168.1.254\n"
printf "$(greenPrint '4)') Go Back to Main Menu\n"
printf "$(redPrint '0)') Exit\n"
printf "\n"
printf "Choose an option:  "
	read -r ans
	case $ans in
		1)
			parallel-ssh -t 300 -i -h clients.txt -I "python3.7" < parser.py - bgw210
			prelimMenu
			;;
		2)
			parallel-ssh -t 300 -i -h clients.txt -I "python3.7" < parser.py - bgw320
			prelimMenu
			;;
		3)
            parallel-ssh -i -h clients.txt "ping -n -c 5 192.168.1.254"
			prelimMenu
			;;
		4)
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

printf "\n"
redPrintln "============ TROUBLESHOOTING ==============="
printf "\n"

printf "What do you have problems with?\n\n"

printf "$(greenPrint '1)') Index out of range\n"
printf "$(greenPrint '2)') Cannot set time\n"
printf "$(greenPrint '3)') Error exit code 255\n"
printf "$(greenPrint '4)') Back to main menu\n"
printf "$(redPrint '0)' ) Exit\n"
printf "Choose an option:  "

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
        4)
            mainMenu
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
    clear
    ~/Desktop/setTime.sh
    printf "$(greenPrint 'Time has been set!')\n"
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
cyanPrint() { printf "${CYAN}%s${RESET}" "$1"; }

redPrintln() { printf "${RED}%s${RESET}\n" "$1"; }
greenPrintln() { printf "${GREEN}%s${RESET}\n" "$1"; }
yellowPrintln() { printf "${YELLOW}%s${RESET}\n" "$1"; }
bluePrintln() { printf "${BLUE}%s${RESET}\n" "$1"; }
magentaPrintln() { printf "${MAGENTA}%s${RESET}\n" "$1"; }
cyanPrintln() { printf "${CYAN}%s${RESET}\n" "$1"; }

mainMenu
