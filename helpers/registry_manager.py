from typing import Dict, Type, Callable, Optional
from dataclasses import dataclass

@dataclass
class HelperConfig:
    tag: str
    class_ref: Type
    enabled: bool = True
    priority: int = 0
    dependencies: list = None

class HelperRegistry:
    """Centralized helper registry for managing and accessing helper classes."""
    def __init__(self):
        self._registered_helpers: Dict[str, HelperConfig] = {}
        self._instantiated_helpers: Dict[str, object] = {}

    def register(self, config: HelperConfig):
        """Register a helper before initializing it."""
        self._registered_helpers[config.tag] = config

    def initialize_all(self, txo, txi, config_tags: list[str] = None):
        """
        Initialize helpers based on config_tags (from konfig.py)
        Respects dependency order and enabled status
        """
        enabled_configs = self._get_sorted_configs(config_tags)
        for config in enabled_configs:
            for dep in (config.dependencies or []):
               if dep not in self._instantiated_helpers:
                   raise ValueError(f"Dependency {dep} not found for {config.tag}")
            helper_instance = config.class_ref(txo, txi)
            self._instantiated_helpers[config.tag] = helper_instance

    def get_helper(self, tag: str) -> Optional[object]:
        """Get an instantiated helper by tag."""
        return self._instantiated_helpers.get(tag)

    def get_all_helpers(self) -> Dict[str, object]:
        """Get all instantiated helpers."""
        return self._instantiated_helpers.copy()

    def _get_sorted_configs(self, tags: list[str]) -> list[HelperConfig]:
        """Sorts registered configs based on priority and enabled status."""
        configs = [self._registered_helpers[tag] for tag in tags
                   if tag in self._registered_helpers and self._registered_helpers[tag].enabled]
        return sorted(configs, key=lambda c: c.priority)