import json
import os
import subprocess
from datetime import datetime, timedelta

def fetch_map_local():
    print("Extracting actual contribution data from local git repository logs...")
    
    # 1. Pull down history from your repository log database
    try:
        log_data = subprocess.check_output(
            ["git", "log", "--all", "--pretty=format:%ad", "--date=short"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8")
    except Exception:
        print("Fallback tracking initialized: building default activity placeholder layout.")
        log_data = ""

    # Count up your commit frequencies per day matching profile properties
    commit_counts = {}
    for line in log_data.splitlines():
        date_str = line.strip()
        if date_str:
            commit_counts[date_str] = commit_counts.get(date_str, 0) + 1

    # 2. Build a standard 53-week timeline tracking scale matrix array grid layout
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=53)
    
    history_data = []
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        commits = commit_counts.get(date_str, 0)
        
        # Translate commit frequency totals into visual level scales 0-4
        if commits == 0:   level = 0
        elif commits < 3:  level = 1
        elif commits < 6:  level = 2
        elif commits < 10: level = 3
        else:              level = 4
            
        history_data.append({
            "date": date_str,
            "level": level
        })
        current_date += timedelta(days=1)
            
    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2)
    print(f"Success! Extracted {len(history_data)} calendar grid blocks into data/contributions.json")

if __name__ == "__main__":
    fetch_map_local()
