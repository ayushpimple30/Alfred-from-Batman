# 🦇 Alfred ~ Your Logical, Memory-Keeping AI Butler
<img width="860" height="645" alt="image" src="https://github.com/user-attachments/assets/80e6d86d-1a7d-4733-a0e0-b593276b611e" />


> "Some men just want to watch the world burn. I just want to remember your name, sir."

**Alfred** is a Python chatbot styled after **Alfred Pennyworth**, Batman's
loyal butler from DC Comics — dry British wit, unshakeable logic, and a
memory that never forgets a fact about you.

Built for two modes:

- 🧠 **Offline logic mode** — works out of the box, no API key. Handles
  arithmetic, remembers facts, answers "who am I" style questions.
- 🤖 **Full Claude mode** — set one env var and Alfred reasons through
  **Claude** for genuinely intelligent, logical, personalised answers.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🗂️ Persistent memory | Facts (name, job, likes, favourites...) saved to `alfred_memory.json`, survive restarts |
| 🧮 Logical answers | Built-in reasoning + arithmetic, no API needed |
| 🎩 In-character | Every reply is Alfred — calm, witty, respectful, precise |
| 🔌 Pluggable brain | Add `ANTHROPIC_API_KEY` and Alfred upgrades to full Claude-powered reasoning |
| 🧹 Memory control | `!memory`, `!forget <key>`, `!reset` commands |

---

## 📁 Project Structure

```
alfred-ai/
├── alfred_ai/
│   ├── __init__.py
│   ├── memory.py      # persistent JSON memory
│   ├── persona.py     # Alfred's character & system prompt
│   ├── brain.py        # logic engine + optional Claude call
│   └── cli.py           # interactive terminal chat loop
├── main.py               # entry point
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/<your-username>/alfred-ai.git
cd alfred-ai
pip install -r requirements.txt
python main.py
```

### Optional: enable full Claude-powered reasoning

```bash
cp .env.example .env
# edit .env and add your key, then:
export ANTHROPIC_API_KEY=your_key_here
python main.py
```

Without the key Alfred still runs perfectly — just on his built-in logic
instead of Claude.

---

## 💬 Example Session

```
============================================================
 ALFRED — your logical, ever-remembering AI butler
============================================================
Good evening. Alfred, at your service. How may I help?
(type 'exit' to leave, '!memory' to see what I remember)

You: my name is Dishan and I live in Mumbai
Alfred: Noted, sir. A pleasure.

You: what's my location
Alfred: Your location is mumbai, if memory serves — and it does.

You: 24 * 7
Alfred: That computes to 168, sir.

You: !memory
Alfred: Here is my record, sir:
- name: Dishan
- location: mumbai

You: exit
Alfred: Very good, sir. I shall be here when you need me. Good day.
```

---

## 🧠 How Memory Works

Alfred watches every message for patterns like:

- `"my name is ..."`
- `"I live in ..."`
- `"I work as ..."`
- `"I like / love ..."`
- `"my favourite <thing> is ..."`

Each match is saved as a fact to `alfred_memory.json`, alongside a rolling
chat history — so the next time you run `python main.py`, Alfred already
knows who you are.

**Commands:**

| Command | Effect |
|---|---|
| `!memory` | Show every fact Alfred has on you |
| `!forget <key>` | Delete one fact, e.g. `!forget job` |
| `!reset` | Wipe all memory and history |
| `exit` / `quit` / `bye` | End the session |

---

## 🛠️ Extending Alfred

- **New logic rules** → add to `try_local_logic()` in `brain.py`
- **New fact patterns** → add a regex to `FACT_PATTERNS` in `brain.py`
- **Change personality** → edit `SYSTEM_PROMPT` in `persona.py`
- **Swap storage** (SQLite, cloud, etc.) → reimplement `Memory` in `memory.py`, keep the same method names

---

## 📜 License

MIT — do whatever you like with it, sir.

---

<p align="center"><i>"It's not who I am underneath, but what I remember, that defines me."</i></p>
