#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TUNNEL_JSON_FILE="dev_tunnel.json"

# Function to get tunnel ID from dev_tunnel.json file
get_tunnel_id_from_json() {
    if [ -f "$TUNNEL_JSON_FILE" ]; then
        TUNNEL_ID=$(jq -r '.tunnel.tunnelId' "$TUNNEL_JSON_FILE" 2>/dev/null)
        if [ "$TUNNEL_ID" != "null" ] && [ -n "$TUNNEL_ID" ]; then
            echo "Found tunnel ID in $TUNNEL_JSON_FILE: $TUNNEL_ID" >&2
            echo "$TUNNEL_ID"
        else
            echo "Warning: Could not extract tunnel ID from $TUNNEL_JSON_FILE" >&2
            return 1
        fi
    else
        echo "Warning: $TUNNEL_JSON_FILE not found" >&2
        return 1
    fi
}

# Get tunnel ID from JSON file
TUNNEL_ID=$(get_tunnel_id_from_json)

# Check if DevTunnel is already running
if pgrep -f "devtunnel host" > /dev/null; then
    echo "DevTunnel is already running (PID: $(pgrep -f 'devtunnel host'))"
    echo "Connect via existing tunnel"
else
    if [ -n "$TUNNEL_ID" ]; then
        echo "Checking if tunnel exists: $TUNNEL_ID"
        
        # Check if the tunnel exists using devtunnel show
        echo "Testing if tunnel $TUNNEL_ID exists..."
        if devtunnel show "$TUNNEL_ID" >/dev/null 2>&1; then
            echo "Tunnel exists, hosting: $TUNNEL_ID"
            devtunnel host "$TUNNEL_ID" --allow-anonymous 2>&1 | tee dev_tunnel.log
        else
            echo "Tunnel not found: $TUNNEL_ID"
            echo "Creating new DevTunnel on port 8000..."
            TUNNEL_JSON=$(devtunnel create --allow-anonymous --json)
            NEW_TUNNEL_ID=$(echo "$TUNNEL_JSON" | jq -r '.tunnel.tunnelId' 2>/dev/null)
            if [ -n "$NEW_TUNNEL_ID" ] && [ "$NEW_TUNNEL_ID" != "null" ]; then
                devtunnel port create "$NEW_TUNNEL_ID" -p 8000
                # devtunnel access create "$NEW_TUNNEL_ID" -p 8000 --anonymous
                devtunnel show "$NEW_TUNNEL_ID" --json > dev_tunnel.json
                devtunnel host "$NEW_TUNNEL_ID" --allow-anonymous 2>&1 | tee dev_tunnel.log
            else
                echo "Failed to create tunnel."
                echo "Checked devtunnel is authenticated"
                echo "devtunnel login"
            fi
        fi
    else
        echo "No tunnel ID found, starting new DevTunnel on port 8000..."

        TUNNEL_JSON=$(devtunnel create --allow-anonymous --json)
        # get the tunnel ID from the JSON variable
        NEW_TUNNEL_ID=$(echo "$TUNNEL_JSON" | jq -r '.tunnel.tunnelId' 2>/dev/null)
        devtunnel port create "$NEW_TUNNEL_ID" -p 8000
        # devtunnel access create "$NEW_TUNNEL_ID" -p 8000 --anonymous
        devtunnel show "$NEW_TUNNEL_ID" --json > dev_tunnel.json
        devtunnel host "$NEW_TUNNEL_ID" --allow-anonymous 2>&1 | tee dev_tunnel.log
    fi
fi
