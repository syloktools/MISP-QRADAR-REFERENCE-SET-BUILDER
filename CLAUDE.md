# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

A collection of Python 3 scripts that pull IOCs (Indicators of Compromise) from a MISP threat intelligence platform and push them into QRadar reference sets via their respective REST APIs.

## Running the Scripts

No build step. Install dependencies, edit credentials/endpoints directly in the script, then run:

```bash
pip install requests pymisp apscheduler urllib3
python3 <script_name>.py
```

## Two Generations of Scripts

**`misp2qradar.py`** — the older, scheduler-based script. It runs continuously on a configurable interval (default 60 minutes) using `apscheduler`. It performs socket connectivity checks before each run, validates the QRadar reference set exists, and auto-detects the set's `element_type`: if `IP`, it filters out non-IPv4 values using a regex before posting.

**`master_qradar_misp_*.py`** — the newer, single-run scripts. Each targets one specific IOC type and exits after one push. Configuration is done by replacing `<placeholder>` tokens at the top of each file. `pymisp` is imported but unused — the MISP API is called directly via `requests`.

| Script | MISP type | MISP category | IOC cleaning |
|---|---|---|---|
| `master_qradar_misp_MD5.py` | `md5` | Payload delivery | none |
| `master_qradar_misp_SHA256.py` | `sha256` | Payload delivery | none |
| `master_qradar_misp_domain.py` | `domain` | Network activity | none |
| `master_qradar_misp_ipdst.py` | `ip-dst` | Network activity | drops values containing `\|` or `/` |
| `master_qradar_misp_ipsrc.py` | `ip-src` | Network activity | drops values containing `\|` or `/` |
| `master_qradar_misp_url.py` | `url` | Network activity | keeps only values starting with `http://`, `https://`, `ftp://`, `git://` |

## API Conventions

- **MISP** — `POST /attributes/restSearch/json` with JSON body; auth via `Authorization` header.
- **QRadar** — `POST /api/reference_data/sets/bulk_load/<set_name>` with a JSON array body; auth via `SEC` header.
- All scripts suppress SSL verification (`verify=False`) and silence the resulting urllib3 warnings.

## Configuration

`misp2qradar.py`: edit the hardcoded variables at the top of the file (`misp_auth_key`, `qradar_auth_key`, `qradar_ref_set`, `misp_server`, `qradar_server`, `frequency`, and the `MISP_PData` query dict).

`master_*` scripts: replace the `<placeholder>` strings inline — `<misp_fqdn>`, `<misp_token>`, `<qradar_fqdn>`, `<reference_set_name>`, `<token>`.
