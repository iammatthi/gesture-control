#!/bin/bash

# Create virtual environment
echo "[INFO] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "[INFO] Installing dependencies..."
pip install -r requirements.txt

# Download mediapipe models
echo "[INFO] Downloading mediapipe models..."
mkdir -p models
wget -q https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task -O models/gesture_recognizer.task

# Get bridge IP
echo "[INFO] Searching for bridge..."
response=$(curl -s "https://discovery.meethue.com/")
if [ $? -ne 0 ]; then
    echo "[Warning] Could not find bridge"
    read -p "Enter bridge IP: " bridge
else
    bridge=$(echo "$response" | jq -r '.[0].internalipaddress')
    echo "[INFO] Found bridge at $bridge"
fi

# Wait for user to press link button
read -p "Press the link button on the bridge and then press any key to continue..."

# Create user
echo "[INFO] Creating user..."
response=$(curl -s -X POST -d '{"devicetype": "mediapipe#mediapipe"}' "http://$bridge/api")
if [[ "$response" != *"success"* ]]; then
    echo "[Warning] Could not create user"
    read -p "Enter username: " username
else
    username=$(echo "$response" | jq -r '.[0].success.username')
    echo "[INFO] Created user $username"
fi

# List all lights
echo "[INFO] Listing lights..."
response=$(curl -s "http://$bridge/api/$username/lights")
echo "Available lights:"
echo -e "ID\tName"
echo "--------------------"
echo "$response" | jq -r 'to_entries[] | "\(.key)\t\(.value.name)"'
read -p "Enter light ID: " light
echo "[INFO] Selected light $light"

# Create config file
cat > config.yml <<EOL
lights:
  bridge: $bridge
  username: $username
  light: $light
EOL

echo "[INFO] Configuration saved to config.yml"
