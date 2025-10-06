from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import fnmatch

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


@dataclass
class PdfTypeRules:
    name: str
    version: str = "1.0"
    description: str = ""
    selection: Dict[str, Any] = field(default_factory=dict)  # filename_patterns, method, pages
    extraction: Dict[str, Any] = field(default_factory=dict)  # selectors
    transforms: List[Dict[str, Any]] = field(default_factory=list)  # ordered ops
    output: Dict[str, Any] = field(default_factory=dict)  # sheet names, labels


class RulesRegistry:
    def __init__(self, rules_dir: Optional[Path] = None):
        self.rules_dir = Path(rules_dir) if rules_dir else None

    def load_type(self, name: str, override_path: Optional[Path] = None) -> PdfTypeRules:
        data = self._load_rules_data(name, override_path)
        return self._parse_rules(data)

    def detect_type(self, pdf_path: Path) -> Optional[str]:
        """Heuristic detection based on filename patterns in available rules.
        More sophisticated detection (first-page sniffing) can be added later.
        """
        if not self.rules_dir or not self.rules_dir.exists():
            return None

        for rules_file in sorted(self.rules_dir.glob("*.yml")) + sorted(self.rules_dir.glob("*.yaml")):
            data = self._safe_load_yaml(rules_file)
            if not data:
                continue
            name = data.get("name")
            patterns = (data.get("selection") or {}).get("filename_patterns") or []
            for pat in patterns:
                if fnmatch.fnmatch(pdf_path.name, pat):
                    return name
        return None

    def _load_rules_data(self, name: str, override_path: Optional[Path]) -> Dict[str, Any]:
        if override_path:
            data = self._safe_load_yaml(override_path)
            if not data:
                raise ValueError(f"Failed to load rules from {override_path}")
            return data

        if not self.rules_dir:
            raise ValueError("Rules directory not configured")

        candidates = [
            self.rules_dir / f"{name}.yml",
            self.rules_dir / f"{name}.yaml",
        ]
        for p in candidates:
            if p.exists():
                data = self._safe_load_yaml(p)
                if not data:
                    raise ValueError(f"Failed to load rules from {p}")
                return data
        raise FileNotFoundError(f"Rules for type '{name}' not found in {self.rules_dir}")

    def _safe_load_yaml(self, path: Path) -> Optional[Dict[str, Any]]:
        if yaml is None:
            raise ImportError("PyYAML is required. Install with: pip install pyyaml")
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _parse_rules(self, data: Dict[str, Any]) -> PdfTypeRules:
        return PdfTypeRules(
            name=data.get("name") or "unknown",
            version=str(data.get("version", "1.0")),
            description=data.get("description", ""),
            selection=data.get("selection") or {},
            extraction=data.get("extraction") or {},
            transforms=data.get("transforms") or [],
            output=data.get("output") or {},
        )


