# incident-alert-forwarder

# Real-Time Incident Response Alert Forwarder & Webhook Engine

A zero-dependency Python alerting engine that parses high-severity security incidents, decorates them with MITRE ATT&CK metadata and actionable remediation playbooks, and delivers rich alert cards directly to team channels (Discord / Slack).

## Features
- **Visual Severity Palette**: Dynamic embed coloring based on threat classification (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`).
- **SOC Action Guidance**: Automatically maps detections to MITRE ATT&CK technique IDs and recommended response playbooks.
- **Zero Third-Party Dependencies**: Powered exclusively by Python standard libraries (`urllib`, `json`, `time`).
- **Interactive Simulator**: Ships with out-of-the-box telemetry simulation for local evaluation.

## Quick Start

### 1. Local Terminal Dry-Run
```bash
python3 event_dispatcher.py


python3 event_dispatcher.py "[https://discord.com/api/webhooks/YOUR_WEBHOOK_URL_HERE](https://discord.com/api/webhooks/YOUR_WEBHOOK_URL_HERE)"
