#!/usr/bin/env python3
"""
Script to update the recent activity section in the GitHub profile README.
Fetches recent repositories, commits, and activities to keep the profile dynamic.
"""

import os
import re
import requests
import datetime
import sys
from typing import List, Dict

def get_github_data(token: str, username: str) -> Dict:
    """Fetch recent GitHub activity data."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get recent repositories
    repos_url = f"https://api.github.com/users/{username}/repos"
    repos_params = {
        "sort": "updated",
        "per_page": 5,
        "type": "owner"
    }
    
    try:
        repos_response = requests.get(repos_url, params=repos_params, headers=headers)
        repos_response.raise_for_status()
        recent_repos = repos_response.json()
    except requests.RequestException as e:
        print(f"Error fetching repositories: {e}")
        recent_repos = []
    
    # Get recent commits (from public activity)
    events_url = f"https://api.github.com/users/{username}/events/public"
    events_params = {"per_page": 10}
    
    try:
        events_response = requests.get(events_url, params=events_params, headers=headers)
        events_response.raise_for_status()
        recent_events = events_response.json()
    except requests.RequestException as e:
        print(f"Error fetching events: {e}")
        recent_events = []
    
    return {
        "repositories": recent_repos,
        "events": recent_events
    }

def format_recent_activity(data: Dict) -> str:
    """Format the recent activity data into markdown."""
    lines = []
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    # Recent repositories section
    if data["repositories"]:
        lines.append("### 📁 Recent Repositories")
        for repo in data["repositories"][:3]:  # Show top 3
            name = repo["name"]
            url = repo["html_url"]
            updated = repo["updated_at"][:10]
            description = repo.get("description", "No description")
            if description and len(description) > 60:
                description = description[:60] + "..."
            
            lines.append(f"- **[{name}]({url})** — {description}")
            lines.append(f"  - Last updated: {updated}")
    
    # Recent activity section
    if data["events"]:
        lines.append("\n### 🔥 Recent Activity")
        activity_count = 0
        for event in data["events"][:5]:  # Show top 5 events
            if activity_count >= 3:  # Limit to 3 activities
                break
                
            event_type = event["type"]
            repo_name = event["repo"]["name"]
            repo_url = f"https://github.com/{event['repo']['name']}"
            created_at = event["created_at"][:10]
            
            if event_type == "PushEvent":
                lines.append(f"- 🚀 **Pushed** to [{repo_name}]({repo_url}) — {created_at}")
            elif event_type == "CreateEvent":
                lines.append(f"- ✨ **Created** [{repo_name}]({repo_url}) — {created_at}")
            elif event_type == "WatchEvent":
                lines.append(f"- 👀 **Starred** [{repo_name}]({repo_url}) — {created_at}")
            
            activity_count += 1
    
    # Add timestamp
    lines.append(f"\n---")
    lines.append(f"*Last updated: {timestamp}*")
    
    return "\n".join(lines) if lines else "_No recent activity found_"

def update_readme(content: str) -> bool:
    """Update the README.md file with new content."""
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            readme = f.read()
        
        # Replace the content between the markers
        pattern = r"(<!--START:recent-->)(.*?)(<!--END:recent-->)"
        replacement = rf"<!--START:recent-->\n{content}\n<!--END:recent-->"
        
        new_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
        
        if new_readme != readme:
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(new_readme)
            return True
        return False
        
    except Exception as e:
        print(f"Error updating README: {e}")
        return False

def main():
    """Main function to update the profile."""
    token = os.environ.get("GH_TOKEN")
    username = os.environ.get("GH_USER", "rajatjc")
    
    if not token:
        print("Error: GH_TOKEN environment variable not set")
        sys.exit(1)
    
    print(f"Updating profile for user: {username}")
    
    # Fetch data
    data = get_github_data(token, username)
    
    # Format content
    content = format_recent_activity(data)
    
    # Update README
    if update_readme(content):
        print("README updated successfully!")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    main()
