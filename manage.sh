#!/bin/bash

# Clonescript Manager
# A simple interactive CLI for managing web clones.

# Colors for better UI
BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Settings
DOWNLOAD_DIR="downloads"
QUEUE_FILE="queue.txt"
CLONER_SCRIPT="cloner.py"

show_header() {
    clear
    echo -e "${BOLD}${BLUE}=======================================${NC}"
    echo -e "${BOLD}${BLUE}       CLONESCRIPT MANAGER v1.0        ${NC}"
    echo -e "${BOLD}${BLUE}=======================================${NC}"
    echo ""
}

list_clones() {
    show_header
    echo -e "${BOLD}Cloned Sites in '$DOWNLOAD_DIR':${NC}"
    if [ ! -d "$DOWNLOAD_DIR" ] || [ -z "$(ls -A "$DOWNLOAD_DIR")" ]; then
        echo -e "${RED}No clones found.${NC}"
    else
        ls -1 "$DOWNLOAD_DIR" | while read -r line; do
            echo -e "  ${GREEN}•${NC} $line"
        done
    fi
    echo ""
    read -p "Press Enter to return to menu..."
}

view_queue() {
    show_header
    echo -e "${BOLD}Current Queue ($QUEUE_FILE):${NC}"
    if [ ! -f "$QUEUE_FILE" ]; then
        echo -e "${RED}$QUEUE_FILE not found.${NC}"
    else
        grep -v '^#' "$QUEUE_FILE" | grep -v '^$' | nl
    fi
    echo ""
    read -p "Press Enter to return to menu..."
}

clone_new() {
    show_header
    echo -e "${BOLD}Clone New Page(s)${NC}"
    echo -e "Enter URLs (separated by space, or one URL):"
    read -p "> " urls
    if [ -z "$urls" ]; then
        echo -e "${RED}URL(s) cannot be empty.${NC}"
        sleep 1
        return
    fi
    
    read -p "Project Name (leave blank for auto): " project
    
    echo -e "\n${BOLD}[*] Starting Cloner (Batch Mode)...${NC}"
    if [ -z "$project" ]; then
        python3 "$CLONER_SCRIPT" $urls
    else
        python3 "$CLONER_SCRIPT" --project "$project" $urls
    fi
    
    echo ""
    read -p "Press Enter to return to menu..."
}

process_queue() {
    show_header
    echo -e "${BOLD}Process Queue${NC}"
    if [ ! -f "$QUEUE_FILE" ]; then
        echo -e "${RED}Error: $QUEUE_FILE does not exist.${NC}"
        sleep 2
        return
    fi
    
    read -p "Assign to specific Project? (leave blank for individual folders): " project
    
    echo -e "\n${BOLD}[*] Starting Batch Cloner...${NC}"
    if [ -z "$project" ]; then
        python3 "$CLONER_SCRIPT" --file "$QUEUE_FILE"
    else
        python3 "$CLONER_SCRIPT" --project "$project" --file "$QUEUE_FILE"
    fi
    
    echo ""
    read -p "Press Enter to return to menu..."
}

while true; do
    show_header
    echo -e "1) ${BOLD}List Cloned Sites${NC}"
    echo -e "2) ${BOLD}Clone New Page/Site${NC}"
    echo -e "3) ${BOLD}Process Queue ($QUEUE_FILE)${NC}"
    echo -e "4) ${BOLD}View Queue${NC}"
    echo -e "5) ${BOLD}Exit${NC}"
    echo ""
    read -p "Choose an option [1-5]: " choice

    case $choice in
        1) list_clones ;;
        2) clone_new ;;
        3) process_queue ;;
        4) view_queue ;;
        5) echo "Goodbye!"; exit 0 ;;
        *) echo -e "${RED}Invalid option.${NC}"; sleep 1 ;;
    esac
done
