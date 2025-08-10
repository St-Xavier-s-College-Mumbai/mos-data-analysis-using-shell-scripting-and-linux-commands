#!/bin/bash

# File paths
input_file="logfiles.log"
output_file="cleaned_logs.csv"

# Add header line to CSV
echo "IP,Timestamp,Method,URL,Status,Size,Referrer,UserAgent,CustomField" > "$output_file"

# Process the log file and append cleaned data
awk '
{
  # Remove [ and ] from timestamp (field 4)
  gsub(/^\[/, "", $4);
  gsub(/\]$/, "", $4);

  # Combine request fields (6-8) which are quoted like "GET /path HTTP/1.0"
  request = $6 " " $7 " " $8;

  # Extract HTTP method and URL from the quoted request
  match(request, /"([A-Z]+) ([^ ]+) HTTP\/[0-9.]+"/, arr);
  method = arr[1];
  url = arr[2];

  # Skip line if method or url not found
  if (method == "" || url == "") next;

  status = $9;
  size = $10;

  # Clean referrer (field 11)
  referrer = $11;
  gsub(/"/, "", referrer);

  # User agent is fields 12 to NF-1 (excluding last custom field)
  user_agent = "";
  for (i = 12; i <= NF - 1; i++) {
    user_agent = user_agent $i " ";
  }
  sub(/[ \t]+$/, "", user_agent);
  gsub(/^"/, "", user_agent);
  gsub(/"$/, "", user_agent);

  custom_field = $NF;

  # Print CSV line
  print $1 "," $4 "," method "," url "," status "," size "," referrer "," "\"" user_agent "\"" "," custom_field;
}
' "$input_file" >> "$output_file"
