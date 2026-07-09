import json
from pathlib import Path

CONFIG_PATH = Path("config.json")

def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_PATH}")

    try:
        with open(CONFIG_PATH, "r") as config_file:
            config = json.load(config_file)

    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in configuration file: {CONFIG_PATH}")

    required_keys = ["repo_path", "idle_duration", "push_enabled", "verbose_level"]

    for key in required_keys:
        if key not in config:
            raise KeyError(f"Missing required configuration key: {key}")
        
    repo_path = Path(config["repo_path"])

    if not repo_path.exists() or not repo_path.is_dir():
        raise ValueError(f"Invalid repository path: {repo_path}")
    
    if not (repo_path / ".git").exists():
        raise ValueError(f"The specified path is not a Git repository: {repo_path}")
    
    if not isinstance(config["idle_duration"], (int, float)) or config["idle_duration"] <= 0 or isinstance(config["idle_duration"], bool):
        raise ValueError("idle_duration must be a positive` number")
    
    if not isinstance(config["push_enabled"], bool):
        raise ValueError("push_enabled must be a boolean value")
    
    if not isinstance(config["verbose_level"], int) or config["verbose_level"] < 0 or config["verbose_level"] > 3:
        raise ValueError("verbose_level must be an integer between 0 and 3")
    

    return config
