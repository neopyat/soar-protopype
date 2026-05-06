# SOAR Prototype

Centralized SOAR (Security Orchestration, Automation and Response) prototype for automated cyber incident detection and response.

The project was developed by Ashurov Sarvar Anvar o'g'li as part of a diploma thesis focused on designing and implementing an automated incident response system for cybersecurity infrastructure.

---

# Features

- SSH brute-force detection
- Automated incident generation
- MITRE ATT&CK mapping
- Remote firewall orchestration
- nftables integration
- SSH log collection
- Event/Incident pipeline architecture
- Playbook-based response logic
- Modular collectors/analyzers/responders
- SQLite-based storage
- Optional ML anomaly module
- Network monitoring support
- System metrics monitoring
- systemd deployment support

---

# Architecture

```text
Attacker
    ↓
Target Host (auth.log)
    ↓
SSH Collector
    ↓
SOAR Pipeline
    ↓
Analyzers
    ↓
Incident Engine
    ↓
Playbooks
    ↓
Remote Responders
    ↓
nftables Mitigation
````

---

# Project Structure

```text
backend/
├── analyzers/
├── collectors/
├── core/
├── models/
├── playbooks/
├── responders/
├── storage/
├── config.json
├── main.py
├── cli_setup.py
├── requirements.txt
└── scripts/
    ├── install.sh
    ├── clean.sh
    ├── uninstall.sh
    ├── setup_firewall.sh
    └── setup_service.sh
```

---

# Requirements

* Ubuntu 22.04+
* Python 3.10+
* nftables
* systemd
* OpenSSH

---

# Installation

Clone repository:

```bash
git clone <repository_url>
cd soar-prototype/backend
```

Run installer:

```bash
sudo bash scripts/install.sh
```

The installer automatically:

* installs dependencies
* creates Python virtual environment
* installs Python packages
* configures nftables
* creates systemd service
* launches configuration wizard

---

# Configuration

Configuration is stored in:

```text
config.json
```

Example configuration:

```json
{
    "loop_interval": 2,
    "debug": false,
    "use_ml": false,
    "enable_blocking": true,

    "ssh_host": "192.168.0.109",
    "ssh_user": "srvr",
    "ssh_log_path": "/var/log/auth.log",

    "enable_network_monitoring": true,
    "enable_system_metrics": true,

    "ddos_threshold": 30,
    "cpu_threshold": 80,

    "siem": "none"
}
```

---

# Service Management

Start service:

```bash
sudo systemctl start soar
```

Stop service:

```bash
sudo systemctl stop soar
```

Restart service:

```bash
sudo systemctl restart soar
```

View logs:

```bash
journalctl -u soar -f
```

Service status:

```bash
sudo systemctl status soar
```

---

# Firewall Integration

The system uses nftables for automated response.

SOAR creates isolated firewall structures:

```text
table inet soar
chain blacklist
```

Blocked IP addresses are dynamically added to the blacklist chain.

---

# Cleanup

Reset runtime state without removing deployment:

```bash
sudo bash scripts/clean.sh
```

This removes:

* runtime logs
* temporary files
* database state
* cached data
* temporary firewall rules

Preserved:

* virtual environment
* config.json
* systemd service
* nftables structure

---

# Uninstall

Completely remove deployment:

```bash
sudo bash scripts/uninstall.sh
```

---

# Demonstrated Capabilities

The prototype was successfully tested against:

* SSH brute-force attacks
* repeated authentication failures
* automated response scenarios
* remote firewall orchestration
* distributed monitoring workflows

The system automatically:

1. collects remote security events
2. normalizes events into a unified pipeline
3. generates incidents
4. maps incidents to MITRE ATT&CK
5. executes response playbooks
6. blocks attacker IP addresses remotely

---

# Current Status

Implemented:

* core pipeline
* SSH log collection
* remote response
* firewall orchestration
* incident processing
* SQLite storage
* deployment scripts

Planned:

* Flask web interface
* dashboard visualization
* advanced SIEM integrations
* extended ML analytics

---

# License

Educational and research use only.

```
```