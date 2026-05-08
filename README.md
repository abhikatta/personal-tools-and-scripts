# Personal Tools

A collection of personal automation scripts and CLI tools written in:

- Bash
- Python

#### The goal of this repository is to maintain a centralized, version-controlled toolkit of utilities that can be exposed globally through `/usr/local/bin`.

---

## Overview

The basic idea is to have all bash/python tools executable globally by adding a symlink to the userspace or globalspace

---

## Project Structure

```text
personal-tools/
├── bin/
│   ├── timer
│   ├── cleanup
│   ├── notes
│   └── weather
│
├── python/
│   └── weather-tool/
│       ├── main.py
│       ├── api.py
│       └── utils.py
│
├── bash/
│   └── cleanup.sh
│
└── README.md
```

---

## Architecture

### `bin/`

Contains executable entrypoints exposed to the system PATH.

These are the commands executed directly from the terminal.

Examples:

```bash
timer
weather
cleanup
```

---

### `python/`

Contains multi-file Python CLI applications and helper modules.

Used for:

- larger CLI tools
- APIs
- validation
- parsing
- application logic

---

### `bash/`

Contains Bash automation scripts and shell utilities.

Used for:

- automation
- orchestration
- filesystem operations
- wrappers
- Unix pipelines

---

## Design Philosophy

- Bash for lightweight automation and orchestration.
- Python for larger CLI tools and application logic.
- Unix-style tooling with symlinked executables.
- Simple and dependency-light workflows.
- Centralized personal developer tooling.

The shell only requires executable entrypoints inside `bin/`.  
Internal implementation details can be organized freely elsewhere in the repository.

---

## Installation

or `~/folder_name` if you dont want it sitting in global space

Clone into `/opt` :

```bash
sudo git clone <repo-url> /opt/personal-tools
```

Create global symlinks:

```bash
sudo ln -sf /opt/personal-tools/bin/* /usr/local/bin/
```

Ensure executables have execute permissions:

```bash
chmod +x /opt/personal-tools/bin/*
```

---

## Notes

- Commands become globally accessible through `/usr/local/bin`.
- Symlinks allow tools to be updated directly from the repository without reinstalling.
- Both Bash and Python executables are supported as long as they:
  - include a valid shebang
  - are executable
  - exist inside `bin/`
