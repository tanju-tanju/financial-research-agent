#!/usr/bin/env python3
import json
import subprocess
import urllib.request

def main():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode().strip()
    project_num = "850196904392"
    engine_id = "aigents"
    base_url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{project_num}/locations/global/collections/default_collection/engines/{engine_id}/assistants/default_assistant/agents"

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Goog-User-Project": "ai-cartridge"
    }

    req = urllib.request.Request(base_url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print(f"Total agents found: {len(data.get('agents', []))}")
        for agent in data.get("agents", []):
            name = agent.get("name", "").split("/")[-1]
            display = agent.get("displayName", "")
            agent_type = agent.get("agentType", "LOW_CODE")
            state = agent.get("state", "UNKNOWN")
            print(f"- {name}: {display} [{agent_type} / {state}]")

    print("\nChecking finance_research agent specifically:")
    finance_url = f"{base_url}/finance_research"
    req_fin = urllib.request.Request(finance_url, headers=headers)
    try:
        with urllib.request.urlopen(req_fin) as resp:
            fin_data = json.loads(resp.read().decode())
            print(json.dumps(fin_data, indent=2))
    except Exception as e:
        print(f"Error fetching finance_research: {e}")

if __name__ == "__main__":
    main()
