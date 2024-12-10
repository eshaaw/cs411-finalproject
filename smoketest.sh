#!/bin/bash

# Define the base URL for the Weather API
BASE_URL="http://localhost:5001"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  response=$(curl -s -X GET "$BASE_URL/api/health")
  echo "Response: $response"  # Add this line to debug
  echo "$response" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the weather API status
check_api_status() {
  echo "Checking weather API status..."
  curl -s -X GET "$BASE_URL/status" | grep -q '"status": "ok"'
  if [ $? -eq 0 ]; then
    echo "API is responding."
  else
    echo "API check failed."
    exit 1
  fi
}

##########################################################
#
# Weather Information Retrieval
#
##########################################################

# Function to get current weather by city
get_weather_by_city() {
  city=$1

  echo "Getting weather for city: $city..."
  response=$(curl -s -X GET "$BASE_URL/weather?city=$city")
  if [ $? -eq 0 ]; then
    echo "Weather data retrieved successfully for $city."
    echo "$response"
  else
    echo "Failed to get weather for $city."
    exit 1
  fi
}

# Function to get weather forecast by city
get_forecast_by_city() {
  city=$1

  echo "Getting weather forecast for city: $city..."
  response=$(curl -s -X GET "$BASE_URL/forecast?city=$city")
  if [ $? -eq 0 ]; then
    echo "Weather forecast retrieved successfully for $city."
    echo "$response"
  else
    echo "Failed to get forecast for $city."
    exit 1
  fi
}

##########################################################
#
# Location-Based Weather Information
#
##########################################################

# Function to get weather by geographical coordinates
get_weather_by_coords() {
  lat=$1
  lon=$2

  echo "Getting weather for coordinates ($lat, $lon)..."
  response=$(curl -s -X GET "$BASE_URL/weather?lat=$lat&lon=$lon")
  if [ $? -eq 0 ]; then
    echo "Weather data retrieved successfully for coordinates ($lat, $lon)."
    echo "$response"
  else
    echo "Failed to get weather for coordinates ($lat, $lon)."
    exit 1
  fi
}

##########################################################
#
# Weather Alerts
#
##########################################################

# Function to get weather alerts
get_weather_alerts() {
  city=$1

  echo "Getting weather alerts for city: $city..."
  response=$(curl -s -X GET "$BASE_URL/alerts?city=$city")
  if [ $? -eq 0 ]; then
    echo "Weather alerts retrieved successfully for $city."
    echo "$response"
  else
    echo "Failed to get weather alerts for $city."
    exit 1
  fi
}

##########################################################
#
# Data Cleanup (Optional)
#
##########################################################

# Function to clear weather data
clear_weather_data() {
  echo "Clearing all weather data..."
  curl -s -X DELETE "$BASE_URL/clear-weather" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Weather data cleared successfully."
  else
    echo "Failed to clear weather data."
    exit 1
  fi
}

##############################################
#
# Test Execution
#
##############################################

# Health check
check_health
check_api_status

# Weather Information Retrieval
get_weather_by_city "Boston"
get_forecast_by_city "Boston"

# Location-Based Weather Information
get_weather_by_coords 42.3601 -71.0589  # Boston coordinates

# Weather Alerts
get_weather_alerts "Boston"

# Data Cleanup
clear_weather_data

echo "All tests passed successfully!"
