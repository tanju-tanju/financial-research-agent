import json
import subprocess
import urllib.request
import urllib.error

def main():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode().strip()
    project_num = "850196904392"
    engine_id = "aigents"
    agent_name = f"projects/{project_num}/locations/global/collections/default_collection/engines/{engine_id}/assistants/default_assistant/agents/finance_research"
    url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{project_num}/locations/global/collections/default_collection/engines/{engine_id}/assistants/default_assistant:streamAssist"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Goog-User-Project": "ai-cartridge"
    }

    payload = {
        "query": {
            "text": "What are the latest revenue estimates and quarterly earnings trends for N26?"
        },
        "agentsConfig": {
            "agent": agent_name
        }
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode()
            events = json.loads(raw, strict=False)
            print(f"Direct FRA Total events: {len(events)}")
            for e in events[:3]:
                print(str(e)[:200])
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}")

if __name__ == "__main__":
    main()
