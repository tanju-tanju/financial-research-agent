import json
import subprocess
import urllib.request
import urllib.error

def query_fra(query_text):
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"], timeout=10).decode().strip()
    except Exception as e:
        return {"error": f"Token error: {e}"}

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
            "text": query_text
        },
        "agentsConfig": {
            "agent": agent_name
        }
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode()
            events = json.loads(raw, strict=False)
            thoughts = []
            final_text = []
            for e in events:
                replies = e.get("answer", {}).get("replies", [])
                for r in replies:
                    content = r.get("groundedContent", {}).get("content", {})
                    t = content.get("text", "")
                    if content.get("thought", False):
                        if t: thoughts.append(t)
                    else:
                        if t: final_text.append(t)
            return {
                "success": True,
                "thoughts": "".join(thoughts),
                "answer": "".join(final_text),
                "event_count": len(events)
            }
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode()}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    res = query_fra("Summarize N26 key financial metrics and funding rounds.")
    print("Success:", res.get("success"))
    print("Event count:", res.get("event_count"))
    print("Answer preview:", res.get("answer")[:300] if res.get("answer") else "No answer")
