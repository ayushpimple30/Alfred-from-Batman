"""
cli.py
------
Interactive terminal chat with Alfred.

Commands:
  !memory      show everything Alfred remembers about you
  !forget key  make Alfred forget one fact
  !reset       wipe all memory and history
  exit / quit  end the session
"""

from .brain import AlfredBrain
from .memory import Memory
from .persona import farewell, greeting


def run(memory_path: str = "alfred_memory.json") -> None:
    memory = Memory(path=memory_path)
    brain = AlfredBrain(memory)

    name = memory.get_fact("name")
    print("=" * 60)
    print(" ALFRED — your logical, ever-remembering AI butler")
    print("=" * 60)
    print(greeting(name))
    print("(type 'exit' to leave, '!memory' to see what I remember)\n")

    while True:
        try:
            user_text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print("Alfred:", farewell())
            break

        if not user_text:
            continue

        if user_text.lower() in ("exit", "quit", "bye"):
            print("Alfred:", farewell())
            break

        if user_text == "!memory":
            print("Alfred: Here is my record, sir:\n" + memory.facts_as_context())
            continue

        if user_text.startswith("!forget "):
            key = user_text.split(" ", 1)[1].strip()
            ok = memory.forget_fact(key)
            msg = f"Very good, '{key}' has been forgotten." if ok else f"No record of '{key}' to forget."
            print("Alfred:", msg)
            continue

        if user_text == "!reset":
            memory.forget_all()
            print("Alfred: As you wish. My memory is now a clean slate.")
            continue

        memory.add_turn("user", user_text)
        reply = brain.respond(user_text)
        memory.add_turn("alfred", reply)
        print("Alfred:", reply)


if __name__ == "__main__":
    run()
