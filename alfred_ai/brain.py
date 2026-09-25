"""
brain.py
--------
Alfred's reasoning core.

- Extracts facts from what the user says ("my name is...", "I like...")
  and stores them via Memory, so Alfred remembers across sessions.
- Answers logic/math questions directly and deterministically.
- If ANTHROPIC_API_KEY is set, routes general questions through Claude
  (as Alfred) for full conversational intelligence. Without a key, falls
  back to a smaller built-in logic/rule engine so the bot still works
  offline, out of the box.
"""

import os
import re
from typing import List, Optional

from .memory import Memory
from .persona import SYSTEM_PROMPT

FACT_PATTERNS = [
    (r"\bmy name is ([A-Za-z][\w .'-]{0,40})", "name"),
    (r"\bi am ([A-Za-z][\w .'-]{0,40}) years old", "age"),
    (r"\bi'?m (\d{1,3}) years old", "age"),
    (r"\bi work as (?:an? )?([A-Za-z][\w .'-]{0,60})", "job"),
    (r"\bi live in ([A-Za-z][\w .'-]{0,60})", "location"),
    (r"\bi like ([A-Za-z][\w ,.'-]{0,80})", "likes"),
    (r"\bi love ([A-Za-z][\w ,.'-]{0,80})", "loves"),
    (r"\bmy favou?rite (\w+) is ([A-Za-z][\w .'-]{0,60})", "favourite"),
]

MATH_RE = re.compile(r"^[\d\s()+\-*/.%]+$")


class AlfredBrain:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")

    # ---------- fact extraction ----------

    def extract_facts(self, text: str) -> List[str]:
        found = []
        lowered = text.lower()
        for pattern, key in FACT_PATTERNS:
            m = re.search(pattern, lowered)
            if not m:
                continue
            if key == "favourite":
                fact_key = f"favourite_{m.group(1)}"
                value = m.group(2).strip(" .")
            else:
                fact_key = key
                value = m.group(1).strip(" .")
            if value:
                self.memory.set_fact(fact_key, value)
                found.append(f"{fact_key} = {value}")
        return found

    # ---------- deterministic logic ----------

    def try_math(self, text: str) -> Optional[str]:
        candidate = text.strip().rstrip("?")
        if MATH_RE.match(candidate) and any(c.isdigit() for c in candidate):
            try:
                # restricted eval: digits/operators only, no names allowed
                result = eval(candidate, {"__builtins__": {}}, {})
                return f"That computes to {result}, sir."
            except Exception:
                return None
        return None

    def try_local_logic(self, text: str) -> Optional[str]:
        t = text.lower().strip()

        math_ans = self.try_math(text)
        if math_ans:
            return math_ans

        if t in ("hi", "hello", "hey", "alfred"):
            name = self.memory.get_fact("name")
            return f"Good day{', ' + name if name else ''}. How may I assist?"

        if "who am i" in t or "what do you know about me" in t:
            return "Here is what I have on record, sir:\n" + self.memory.facts_as_context()

        if t.startswith("what is my ") or t.startswith("what's my "):
            key = t.split("my ", 1)[1].strip(" ?")
            key_norm = key.replace(" ", "_")
            value = self.memory.get_fact(key_norm) or self.memory.get_fact(key)
            if value:
                return f"Your {key} is {value}, if memory serves — and it does."
            return f"I have no record of your {key} yet, sir. Do tell me."

        if "thank" in t:
            return "You are very welcome, sir. It is, after all, the job."

        return None

    # ---------- Claude-backed reasoning (optional) ----------

    def ask_claude(self, text: str) -> Optional[str]:
        if not self.api_key:
            return None
        try:
            import requests
        except ImportError:
            return None

        context = self.memory.facts_as_context()
        history = self.memory.recent_history(8)
        history_text = "\n".join(f"{h['role']}: {h['content']}" for h in history)

        prompt = (
            f"Known facts about the user:\n{context}\n\n"
            f"Recent conversation:\n{history_text}\n\n"
            f"User's new message: {text}"
        )

        try:
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-6",
                    "max_tokens": 600,
                    "system": SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=30,
            )
            resp.raise_for_status()
            payload = resp.json()
            parts = [b["text"] for b in payload.get("content", []) if b.get("type") == "text"]
            return "\n".join(parts).strip() or None
        except Exception:
            return None

    # ---------- entry point ----------

    def respond(self, text: str) -> str:
        self.extract_facts(text)

        claude_answer = self.ask_claude(text)
        if claude_answer:
            return claude_answer

        local_answer = self.try_local_logic(text)
        if local_answer:
            return local_answer

        return (
            "A fair question, sir, but beyond my local reasoning without a "
            "connection to my fuller faculties. Set ANTHROPIC_API_KEY for "
            "the complete Alfred experience — in the meantime, I can help "
            "with arithmetic, and I am always listening and remembering."
        )
