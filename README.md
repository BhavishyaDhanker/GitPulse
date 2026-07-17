# GitPulse V0.1

A lightweight background utility that watches a single Git repository and automatically commits (and optionally pushes) your changes once the repository goes idle for a configurable amount of time.

Think of it as a safety net for people who forget to commit — GitPulse notices when you've stopped editing and quietly saves your progress to Git for you.

## Features

- Watches one local Git repository for file creations, modifications, and deletions.

- Debounces rapid changes — waits until you've been idle for a configurable duration before acting, instead of committing on every save.

- Automatically stages, commits, and (optionally) pushes changes when idle.

- Skips committing if there's nothing to commit.

- Logs every action with timestamps, both to the terminal and to a `GitLogs.txt` file, for later review.

- Uses Ctrl + C to close the project.

## Requirements

- Python 3.9+

- An existing local Git repository (with a remote configured, if you want push enabled)

- Dependencies listed in `requirements.txt`

## Installation

```
git clone \<your-repo-url\>  
cd GitPulse  
pip install -r requirements.txt
```

## Configuration

GitPulse is configured via a `config.json` file in the project root:

```
\{  
    "repo\_path": "/path/to/your/repo",  
    "idle\_duration": 120,  
    "push\_enabled": true,  
    "verbose\_level": 2  
\}
```

| Field | Type | Description |
| - | - | - |
| `repo\_path` | string | Absolute path to the Git repository to watch. Must exist and contain a `.git` folder. |
| `idle\_duration` | integer | Seconds of inactivity to wait before triggering a commit. |
| `push\_enabled` | boolean | Whether to run `git push` after committing. Set to `false` to commit locally only. |
| `verbose\_level` | integer (0–3) | Logging verbosity. `0` = errors only, `1` = warnings+, `2` = info+, `3` = debug+ . |


## Usage

Run from a real terminal — not an editor's "Run" button/output panel, since some of those don't forward Ctrl+C correctly:

```
python main.py
```

GitPulse will start watching the configured repository. Edit files as normal; once you stop for `idle\_duration` seconds, GitPulse will automatically add, commit, and (if enabled) push your changes.

To stop GitPulse, press `Ctrl+C` in the terminal it's running in. It will cancel any pending idle timer, attempt one final commit immediately, and then exit cleanly.

All activity is logged to `GitLogs.txt` in the project root, as well as printed to the terminal.

## Project Structure

```
GitPulse/  
├── main.py          \# Entry point — loads config, sets up logging, starts/stops the watcher  
├── monitor.py        \# Filesystem watcher (watchdog) + idle-debounce timer logic  
├── git\_handler.py    \# Git operations (status check, add, commit, push) via subprocess  
├── config.py          \# Loads and validates config.json  
├── config.json        \# User-editable configuration (not committed if it contains machine-specific paths)  
├── requirements.txt  
└── README.md
```

## Known Limitations (V0.1 scope)

This is an intentionally minimal first version. The following are **not** yet supported, by design:

- Watching multiple repositories at once

- A GUI or system tray icon

- AI-generated commit messages (currently uses a fixed message)

- Desktop notifications

- Auto-start on system boot

- Scheduled (time-of-day) commits — only idle-based triggering is supported

- Detailed classification of push failures (network vs. auth, etc.) — raw Git error output is logged instead

These are candidates for future versions (V0.5+).

## Troubleshooting

- **Ctrl+C doesn't stop the program:** Make sure you're running `python main.py` in a real terminal (not through an IDE's "Run"/"Code Runner" button), and that the terminal window has focus when you press Ctrl+C.

- **"Invalid repository path" or "not a Git repository" error on startup:** Double-check `repo\_path` in `config.json` points to a folder that exists and contains a `.git` subfolder.

- **Push fails repeatedly:** Check `GitLogs.txt` for the raw Git error — common causes are no network connection, missing/expired credentials, or no remote configured.

