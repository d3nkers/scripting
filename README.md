# Scripting Lab – Tools, Helpers & CTF Scripts

This repository contains a collection of small scripts and helpers I've written during my journey through cybersecurity, penetration testing, and system administration.  
Some of these were created during Capture The Flag (CTF) challenges, others for automation or general tooling.

> **Disclaimer:** These scripts are intended for educational and demonstrative purposes only. Do not use them in production environments unless you fully understand what they do.

---
 Script name             | Description                                                  | Language |
|-------------------------|--------------------------------------------------------------|----------|
| `monitormode.py`        | Enables monitor mode for Wi-Fi pentesting on boot            | Python   |
| `dnsenumeration.py`     | Simple DNS recon tool with automated dig/nslookup queries    | Python   |
| `toolinstaller.py`      | Quick setup of essential pentest tools on fresh Linux VMs    | Bash     |
| `xss-scanner.py`        | Basic GET XSS enumeration tool for web pentests              | Python   |
| `diskusage-report.sh`   | Generates disk usage reports for root and mounted partitions | Bash     |
| `logrotate-check.sh`    | Lists logrotate configs and highlights misconfigurations     | Bash     |
| `user-audit.sh`         | Lists system users, sudo access, last login and lock status  | Bash     |
| `backup-home.sh`        | Creates timestamped backups of user home directory           | Bash     |
| `service-monitor.sh`    | Monitors and restarts critical services if they crash        | Bash     |

> For a full list, see the file comments or explore each script individually.

---

## What you'll find here

- Lightweight tools I use during pentests or practice labs
- Quick automations for common tasks
- Reusable snippets that can be adapted to new challenges
- Scripts that reflect my learning path and skill growth

---

## Work in Progress

This repository is updated as I grow and sharpen my skills. Some scripts are quick & dirty by design (e.g. CTF tools), while others follow cleaner standards.

---

## Responsibility

Please use responsibly. Hacking and scanning tools should **never be run on systems without permission**. I do not take any responsibility for misuse.

---

## License

MIT License

---

## About Me
I'm a hands-on cybersecurity enthusiast transitioning into professional red teaming and system hardening. I learn by doing, and this repo is one of the ways I document and share my progress.
