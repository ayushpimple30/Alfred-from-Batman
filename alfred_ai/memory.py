"""
memory.py
---------
Persistent memory for Alfred. Stores user facts (name, likes, job, etc.)
and rolling chat history in a local JSON file — survives across sessions.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List


class Memory:
    def __init__(self, path: str = "alfred_memory.json", max_history: int = 200):
        self.path = path
        self.max_history = max_history
        self.data: Dict[str, Any] = {"facts": {}, "history": []}
        self._load()

    # ---------- persistence ----------

    def _load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, OSError):
                self.data = {"facts": {}, "history": []}
        self.data.setdefault("facts", {})
        self.data.setdefault("history", [])

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    # ---------- facts ----------

    def set_fact(self, key: str, value: str) -> None:
        self.data["facts"][key] = value
        self.save()

    def get_fact(self, key: str) -> str:
        return self.data["facts"].get(key, "")

    def all_facts(self) -> Dict[str, str]:
        return dict(self.data["facts"])

    def forget_fact(self, key: str) -> bool:
        if key in self.data["facts"]:
            del self.data["facts"][key]
            self.save()
            return True
        return False

    def forget_all(self) -> None:
        self.data["facts"] = {}
        self.data["history"] = []
        self.save()

    # ---------- history ----------

    def add_turn(self, role: str, content: str) -> None:
        self.data["history"].append(
            {
                "role": role,
                "content": content,
                "ts": datetime.now().isoformat(timespec="seconds"),
            }
        )
        # keep history bounded
        if len(self.data["history"]) > self.max_history:
            self.data["history"] = self.data["history"][-self.max_history :]
        self.save()

    def recent_history(self, n: int = 12) -> List[Dict[str, str]]:
        return self.data["history"][-n:]

    def facts_as_context(self) -> str:
        facts = self.all_facts()
        if not facts:
            return "No known facts about the user yet."
        return "\n".join(f"- {k}: {v}" for k, v in facts.items())
