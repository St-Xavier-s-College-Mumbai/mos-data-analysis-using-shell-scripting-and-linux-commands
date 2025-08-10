import matplotlib.pyplot as plt
import pandas as pd
import os
import random
import numpy as np


#1)✅
# Read data from the analysis result file
methods = []
counts = []

with open('analysis_results/top_methods.txt') as f:
    for line in f:
        count, method = line.strip().split()
        counts.append(int(count))
        methods.append(method)


print("Methods:",methods)
print("Counts:",counts)
# Plot
plt.bar(methods, counts, color='skyblue')
plt.title('Top 5 HTTP Methods Frequency')
plt.xlabel('HTTP Method')
plt.ylabel('Count')
plt.ylim(248000, 252000)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('/mnt/hgfs/vm_share/visualize/top_methods1.png')
plt.close()

#2)

counts = []

with open('analysis_results/top_ips.txt') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        count = int(parts[0])
        counts.append(count)


one_count = counts.count(1)
two_count = counts.count(2)

print(f"one_count = {one_count}, two_count = {two_count}")


labels=['1 Request','2 Request']
sizes=[one_count,two_count]
colors=['lightblue','lightcoral']

plt.pie(sizes,labels=labels,colors=colors,autopct='%1.1f%%',startangle=140)
plt.title('Proportion of IPs by Number of Requests')
plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
plt.tight_layout()

#3)✅


status_codes = []
counts = []

with open('analysis_results/status_codes.txt') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2:
            count, code = parts
            counts.append(int(count))
            status_codes.append(code)

plt.barh(status_codes, counts, color='skyblue')
plt.xlim(142000, 144000)
#plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylabel('HTTP Status Codes')
plt.xlabel('Counts')
plt.title('Distribution of HTTP Status Codes')
plt.tight_layout()

plt.savefig('/mnt/hgfs/vm_share/visualize/ip_request_histogram.png')
plt.close()


#4)✅
methods = []
error_rates = []

import matplotlib.pyplot as plt

methods = []
error_rates = []

with open('analysis_results/method_error_rates.txt', 'r') as f:
    for line in f:
        # skip empty lines or lines starting with 'Method'
        if not line.strip() or line.startswith('Method'):
            continue
        parts = line.strip().split(',')
        if len(parts) < 4:
            continue
        methods.append(parts[0])
        error_rates.append(float(parts[3]))

plt.figure(figsize=(7,7))
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']  # Customize colors if needed

plt.pie(error_rates, labels=methods, autopct='%1.1f%%', startangle=140, colors=colors, wedgeprops={'edgecolor': 'black'})

plt.title('HTTP Method Error Rate Distribution')
plt.tight_layout()

plt.savefig('/mnt/hgfs/vm_share/visualize/method_error_rate_pie.png')
plt.close()

#5)
import matplotlib.pyplot as plt

timestamps = []
counts = []

with open('analysis_results/requests_per_hour.txt', 'r') as f:
    for line in f:
        ts, count = line.strip().split()
        timestamps.append(ts)
        counts.append(int(count))

plt.figure(figsize=(12,6))
plt.plot(timestamps, counts, marker='o', linestyle='-', color='b')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Date and Hour')
plt.ylabel('Number of Requests')
plt.title('Request Volume Over Time (Hourly)')
plt.tight_layout()
plt.grid(True)
#plt.savefig('analysis_results/requests_over_time.png')
#plt.close()
plt.savefig('/mnt/hgfs/vm_share/visualize/requests_over_time.png')
plt.close()

#6)✅
# Read the breakdown file
browsers = []
counts = []

with open('analysis_results/user_agent_breakdown.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(',')
        if len(parts) != 2:
            continue
        browsers.append(parts[0])
        counts.append(int(parts[1]))


# Custom label function: show count + percentage
def autopct_format(pct, all_vals):
    total = sum(all_vals)
    val = int(round(pct * total / 100.0))
    return f"{val:,} ({pct:.0f}%)"  # comma-separated count + rounded %

plt.figure(figsize=(8, 8))
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']

plt.pie(
    counts,
    labels=browsers,
    autopct=lambda pct: autopct_format(pct, counts),
    startangle=140,
    colors=colors
)

plt.title('User Agent Breakdown (Count + %)')
plt.tight_layout()

# Save to file
plt.savefig('/mnt/hgfs/vm_share/visualize/requests_over_time.png')
plt.close()

#7)

methods = []
avg_sizes = []

with open('analysis_results/method_avg_size.txt') as f:
    for line in f:
        if not line.strip():
            continue
        method, avg = line.strip().split(',')
        methods.append(method)
        avg_sizes.append(float(avg))

plt.figure(figsize=(8,5))
plt.hlines(y=methods, xmin=min(avg_sizes)-5, xmax=max(avg_sizes)+5, color='lightgray', alpha=0.7)
plt.plot(avg_sizes, methods, "o", markersize=8, color="dodgerblue")

for method, size in zip(methods, avg_sizes):
    plt.text(size + 0.1, method, f'{size:.2f}', va='center')

plt.xlabel('Average Response Size (bytes)')
plt.title('Average Response Size per HTTP Method (Lollipop Chart)')
plt.tight_layout()
plt.savefig('/mnt/hgfs/vm_share/visualize/requests_over_time.png')
plt.close()


#8)

'''# Paths
input_file = "analysis_results/top_urls.txt"
output_dir = "analysis_results"

# Load data
df = pd.read_csv(input_file, header=None, names=["URL", "Count"])
# Keep top 5 for clarity
df = df.nlargest(5, "Count")

# Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(df["URL"], df["Count"], color=colors)

y_max = df["Count"].max()
plt.ylim(0, y_max + 5000)


# Add labels on bars
for bar, count in zip(bars, df["Count"]):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, str(count),
             ha='center', fontsize=9)

plt.xlabel("URL")
plt.ylabel("Request Count")
plt.title("Top Requested URLs (Random Order & Colors)")
plt.xticks(rotation=30, ha='right')
plt.tight_layout()'''

urls = []
counts = []

with open('analysis_results/top_urls.txt', 'r') as f:
    for line in f:
       	url, count = line.strip().split(',')
    urls.append(url)
    counts.append(int(count))

max_ylim = 210000  # set max y limit (a bit above max count 200383)

max_count=max(counts)
# Clip counts to max_ylim so bars don’t go above y-limit
clipped_counts = [min(c, max_ylim) for c in counts]


# Scale counts so the max fits exactly in max_ylim
scaled_counts = [c * max_ylim / max_count for c in counts]
colors = ['#ffb3ba', '#bae1ff', '#baffc9', '#ffffba', '#ffdfba']

plt.figure(figsize=(10,6))
bars = plt.bar(urls, scaled_counts, color=colors)

plt.ylim(0, max_ylim)
plt.title('Top Requested URLs')
plt.ylabel('Request Counts')
plt.xlabel('URL')

# Adds value labels on bars
for bar, orig, scaled in zip(bars, counts, scaled_counts):
    height = bar.get_height()
    label = f"{orig}"
    if orig != scaled:  # Means scaled
        label += '*'
    plt.text(bar.get_x() + bar.get_width()/2, height + max_ylim*0.02, label, ha='center', va='bottom')

plt.tight_layout()
# Save
plt.savefig('/mnt/hgfs/vm_share/visualize/top_urls_scaled_bar.png')
plt.close()

print(f"Bar chart saved to: /mnt/hgfs/vm_share/visualize/top_urls_scaled__bar.png")
 
#9)✅

counts = []
urls = []

with open('analysis_results/error_url_counts.txt', 'r') as file:
    for line in file:
        parts = line.strip().split()  # splits on any whitespace
        if len(parts) < 2:  # require at least count and URL
            continue
        counts.append(int(parts[0]))
        urls.append(parts)

# Reverse the data so highest count is at top of plot
counts = counts[:4]
urls = urls[:4]


plt.figure(figsize=(8,5))
colors = ['red'] * len(counts)  # all red bars

plt.barh(urls, counts, color=colors)
plt.xlabel('Number of Error Responses')
plt.title('Top URLs with Most Error Responses')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('/mnt/hgfs/vm_share/visualize/error_url_counts.png')
plt.close()



#10)✅

browsers = ["Other", "Firefox"]
mobile_counts = [400710, 100153]
desktop_counts = [399337, 99800]

x = np.arange(len(browsers))  # positions for groups
width = 0.35  # bar width

fig, ax = plt.subplots(figsize=(8, 5))

# Bars for Mobile and Desktop side by side
bars_mobile = ax.bar(x - width/2, mobile_counts, width, label='Mobile', color='skyblue')
bars_desktop = ax.bar(x + width/2, desktop_counts, width, label='Desktop', color='salmon')

# Axis labels and chart title
ax.set_xlabel('Browser')
ax.set_ylabel('Request Count')
ax.set_title('Requests by Browser and Device Type')
ax.set_xticks(x)
ax.set_xticklabels(browsers)
ax.legend()

# Add value labels on top of bars
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:,}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

add_labels(bars_mobile)
add_labels(bars_desktop)

plt.tight_layout()
plt.savefig('/mnt/hgfs/vm_share/visualize/plot_browser_device.png')
plt.close()
