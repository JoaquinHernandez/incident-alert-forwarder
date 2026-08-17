import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

class IncidentEventDispatcher:
    def __init__(self, templates_path="alert_templates.json"):
        if not os.path.exists(templates_path):
            print(f"[-] Config template '{templates_path}' not found.")
            sys.exit(1)

        with open(templates_path, "r") as f:
            self.data = json.load(f)

        self.colors = self.data.get("severity_colors", {})
        self.mock_events = self.data.get("mock_events", [])

    def create_discord_payload(self, event):
        """Builds a formatted rich embed message card."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        color = self.colors.get(event["severity"], 3447003)

        payload = {
            "username": "Blue Team SIEM SOC Bot",
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/9446/9446736.png",
            "embeds": [
                {
                    "title": event["title"],
                    "description": event["description"],
                    "color": color,
                    "fields": [
                        {"name": "Severity", "value": f"`{event['severity']}`", "inline": True},
                        {"name": "MITRE ATT&CK", "value": f"`{event['mitre_technique']}`", "inline": True},
                        {"name": "Asset / Origin", "value": f"`{event['source']}`", "inline": False},
                        {"name": "SOC Playbook Action", "value": f"_{event['recommended_action']}_", "inline": False}
                    ],
                    "footer": {
                        "text": f"Incident Telemetry Forwarder • {now}"
                    }
                }
            ]
        }
        return payload

    def send_webhook(self, webhook_url, payload):
        """Dispatches JSON payload to the remote HTTP webhook."""
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=data_bytes,
            headers={
                "User-Agent": "Security-Incident-Forwarder/1.0",
                "Content-Type": "application/json"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status in (200, 204)
        except urllib.error.HTTPError as e:
            print(f"[-] HTTP error while transmitting alert: {e.code} - {e.reason}")
            return False
        except Exception as e:
            print(f"[-] Network connection error: {e}")
            return False

    def run_simulator(self, webhook_url=None):
        print("=" * 70)
        print("⚡ Real-Time Blue Team Incident Forwarder & Webhook Engine")
        print("=" * 70)

        if not webhook_url:
            print("[i] No Webhook URL supplied. Launching in Terminal Dry-Run Simulator Mode.")
            print("[i] Tip: Run with an active Discord/Slack webhook URL to test live channels.\n")
        else:
            print(f"[+] Dispatching live alerts to target webhook channel...\n")

        for idx, event in enumerate(self.mock_events, start=1):
            print(f"[{idx}/{len(self.mock_events)}] Processing Security Event -> {event['title']}")
            payload = self.create_discord_payload(event)

            if webhook_url:
                success = self.send_webhook(webhook_url, payload)
                status = "✓ DISPATCHED" if success else "❌ FAILED"
                print(f"    Status: {status} | Severity: {event['severity']}")
            else:
                # Pretty print local preview
                print(f"    • Severity: {event['severity']}")
                print(f"    • Source: {event['source']}")
                print(f"    • Mitre Technique: {event['mitre_technique']}")
                print(f"    • Action: {event['recommended_action']}")
                print("    [Simulated Card Output Rendered Successfully]")

            time.sleep(1.5)

        print("\n[+] Telemetry forwarding simulation completed.")

if __name__ == "__main__":
    # If a webhook URL is passed via command line argument, use it; otherwise dry run
    cli_webhook = sys.argv[1] if len(sys.argv) > 1 else None
    dispatcher = IncidentEventDispatcher()
    dispatcher.run_simulator(cli_webhook)
