"""Configuration loader for Square Cafe Report."""
import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Dictionary containing configuration

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}\n"
            f"Please copy config.example.yaml to config.yaml and add your Square credentials."
        )

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    # Validate required fields
    required_fields = ['square.access_token', 'square.environment', 'square.locations']
    for field in required_fields:
        keys = field.split('.')
        value = config
        for key in keys:
            value = value.get(key)
            if value is None:
                raise ValueError(f"Missing required configuration: {field}")

    return config


def get_square_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Extract Square-specific configuration."""
    return config.get('square', {})


def get_locations(config: Dict[str, Any]) -> list:
    """Extract location configurations."""
    return config.get('square', {}).get('locations', [])


def get_timezone(config: Dict[str, Any]) -> str:
    """Get timezone setting."""
    return config.get('timezone', 'America/Los_Angeles')


def get_peak_hours(config: Dict[str, Any]) -> Dict[str, int]:
    """Get peak hours configuration."""
    return config.get('peak_hours', {'start': 11, 'end': 14})
