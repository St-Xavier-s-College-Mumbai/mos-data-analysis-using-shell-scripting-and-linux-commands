#!/bin/bash

# File variables
cleaned_file="cleaned_logs.csv"
output_dir="analysis_results"
mkdir -p "$output_dir"

#✅ Insight 1: Top 5 HTTP Methods frequency
awk -F',' 'NR>1 {print $3}' "$cleaned_file" | sort | uniq -c | sort -nr | head -5 > "$output_dir"/top_methods.txt

# Insight #2:Find which IP addresses made the most requests
awk -F',' 'NR>1 {print $1}' "$cleaned_file" | sort | uniq -c | sort -nr | head -20 > "$output_dir"/top_ips.txt

#✅Insight #3: Top Status Codes and Their Counts from your logs.
# Extract HTTP status codes from cleaned_logs.csv (5th column), count and sort
cut -d',' -f5 "$cleaned_file" | sort | uniq -c | sort -nr > "$output_dir"/status_codes.txt

#✅Insight 4  Error Rate by HTTP Method
#Error requests per method: status codes 400-599
awk -F',' '{ method=$3; status=$5; if (status ~ /^[45][0-9][0-9]$/) { error_count[method]++;} total_count[method]++;
}
END {
  for (m in total_count) {
    e = error_count[m]+0;
    t = total_count[m];
    rate = (e/t)*100;
    printf "%s,%d,%d,%.2f\n", m, e, t, rate;
  }
}
' "$cleaned_file" | sort -t',' -k4 -nr > "$output_dir"/method_error_rates.txt

#Insight 5:  Request volume over time (trend analysis)
awk -F',' '
NR > 1 {
  # Split Timestamp by colon (:)
  split($2, t, ":");
  # t[1] is date (27/Dec/2037), t[2] is hour (12)
  hour = t[1] ":" t[2];
  count[hour]++;
}'
END{
  for (h in count)
    print h, count[h];
}' "$cleaned_file" | sort > "$output_dir"/requests_per_hour.txt


#✅ Insight #6:User Agents Breakdown
#Count requests per exact User-Agent string and sort by frequency
awk -F',' '
NR > 1 {
    # Rebuild UA
    ua = $(8)
    for (i = 9; i <= NF - 1; i++) ua = ua "," $(i)
    gsub(/^"|"$/, "", ua)

    l = tolower(ua)
    if (l ~ /chrome/ && l !~ /edg/ && l !~ /opr/) browser = "Chrome"
    else if (l ~ /firefox/) browser = "Firefox"
    else if (l ~ /safari/ && l !~ /chrome/) browser = "Safari"
    else if (l ~ /edg/) browser = "Edge"
    else if (l ~ /opr/ || l ~ /opera/) browser = "Opera"
    else browser = "Other"

    count[browser]++
}
END {
    for (b in count) print b "," count[b]
}'  "$cleaned_file" > "$output_dir"/user_agent_breakdown.txt


#✅ Insight 7: Average Response Size per HTTP Method.

awk -F, 'NR>1 {
    sum[$3] += $6
    count[$3]++
}
END {
    for (method in sum) {
        avg = sum[method] / count[method]
        print method "," avg
    }
}' "$cleaned_file" > "$output_dir"/method_avg_size.txt

#✅ Insight 8: Top requested URLs
awk -F, 'NR>1 {count[$4]++} END {for (u in count) print u","count[u]}' "$cleaned_file"  | sort -t, -k2,2nr > "$output_dir"/top_urls.txt

#✅ Insight 9:  Identify URLs With the Most Error Responses
awk -F',' '$6 ~ /^4/ || $6 ~ /^5/ {print $4,$6}' "$cleaned_file" | sort | uniq -c | sort -nr | head -10 > "$output_dir"/error_url_counts.txt

#✅ Insight 10:  Investigate correlations between the CustomField and error incidents in web server logs
awk -F, 'NR>1 {
    ua = $8
    browser = "Other"
    device = "Desktop"

    if (ua ~ /Chrome/ && ua !~ /Chromium/) browser = "Chrome"
    else if (ua ~ /Firefox/) browser = "Firefox"
    else if (ua ~ /Safari/ && ua !~ /Chrome/) browser = "Safari"
    else if (ua ~ /Edge/) browser = "Edge"
    else if (ua ~ /OPR|Opera/) browser = "Opera"
    else if (ua ~ /MSIE|Trident/) browser = "Internet Explorer"
    if (ua ~ /Mobile|Android|iPhone|iPad|iPod/) device = "Mobile"
    browser_device[browser","device]++
}
END {
    for (bd in browser_device)
        print bd "," browser_device[bd]
}' "$cleaned_file" | sort -t, -k3 -nr > "$output_dir"/custom_field_error.txt
