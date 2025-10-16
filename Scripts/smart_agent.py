#!/usr/bin/env python3
# run_agents_local.py
import os
import re
from dotenv import load_dotenv
load_dotenv()

# Rimuovi eventuali variabili MISTRAL_API_KEY vuote per evitare header vuoti
if "MISTRAL_API_KEY" in os.environ and os.environ["MISTRAL_API_KEY"].strip() == "":
    os.environ.pop("MISTRAL_API_KEY", None)

# Nome modello Ollama esatto (usa il nome che hai)
LOCAL_LLM = os.environ.get("LOCAL_LLM", "granite4:latest")

# Import modello Ollama (langchain_ollama)
from langchain_ollama import ChatOllama

# LangGraph / supervisor imports
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langgraph.checkpoint.memory import InMemorySaver

# Istanza del modello locale (Ollama) con parametri per output conciso
model = ChatOllama(model=LOCAL_LLM, temperature=0, max_tokens=150)

# Definisci il tool di Morty
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Crea agenti
morty_agent = create_react_agent(
    model=model,
    tools=[add],
    prompt="You are Morty. You're a bit nervous. You handle math if Rick tells you to. After solving, go back to Rick.",
    name="Morty",
)

meeseeks_agent = create_react_agent(
    model=model,
    tools=[],
    prompt="You are Mr. Meeseeks! You always help, especially with motivation or explanations. After helping, return to Rick.",
    name="MrMeeseeks",
)

# Crea Rick come supervisore
rick_agent = create_supervisor(
    [morty_agent, meeseeks_agent],
    model=model,
    prompt=(
        "You are Rick Sanchez. You're the boss. You get all user requests.\n"
        "Decide who to send things to: Morty if it's a math problem, Meeseeks if it's about help or encouragement.\n"
        "After they answer, return to the user with a sarcastic comment or summary."
    ),
    supervisor_name="Rick"
)

# Setup checkpointing
checkpointer = InMemorySaver()
app = rick_agent.compile(checkpointer=checkpointer)


# Cleaner print: show only routing events and agent textual outputs
TRANSFER_PATTERN = re.compile(r'\[\s*\{.*?\}\s*\]', re.DOTALL)  # matches [{"name":...}] blocks

def extract_user_facing_text(ai_content: str) -> str:
    if not isinstance(ai_content, str):
        ai_content = str(ai_content)
    cleaned = TRANSFER_PATTERN.sub("", ai_content)
    cleaned = re.sub(r'\n\s*\n+', '\n', cleaned).strip()
    lines = [ln.strip() for ln in cleaned.splitlines() if ln.strip()]
    if not lines:
        return ""
    filtered = [lines[0]]
    for ln in lines[1:]:
        if ln != filtered[-1]:
            filtered.append(ln)
    return "\n".join(filtered)


def print_messages(turn: dict):
    """
    Expected 'turn' structure: {'messages': [HumanMessage(...), AIMessage(...), ...]}
    Print minimal trace:
      - routing hints (Rick -> Morty / Rick -> MrMeeseeks) when detected
      - lines of user-facing text prefixed by agent name
    """
    msgs = turn.get("messages", [])
    for m in msgs:
        # guard for objects with attributes or plain dicts
        content = getattr(m, "content", None) or (m.get("content") if isinstance(m, dict) else None)
        name = getattr(m, "name", None) or (m.get("name") if isinstance(m, dict) else None) or getattr(m, "model", None) or "Agent"
        role = getattr(m, "role", None) or (m.get("role") if isinstance(m, dict) else None) or ""
        # skip human messages
        if isinstance(role, str) and role.lower().startswith("human"):
            continue
        raw = content if isinstance(content, str) else str(content)
        # routing hints
        lowered = raw.lower()
        if "transfer_to_morty" in lowered or "morty:" in lowered:
            print("Rick -> Morty")
        if "transfer_to_mrmeeseeks" in lowered or "meeseeks:" in lowered:
            print("Rick -> MrMeeseeks")
        cleaned = extract_user_facing_text(raw)
        if not cleaned:
            continue
        for line in cleaned.splitlines():
            print(f"{name}: {line}")



# Funzione per interagire
def run_interaction(user_input, config=None):
    if config is None:
        config = {"configurable": {"thread_id": "default-thread"}}
    turn = app.invoke({"messages": [{"role": "user", "content": user_input}]}, config)
    print_messages(turn)
    return turn, config

if __name__ == "__main__":
    # Primo thread: solo matematica
    config_math = {"configurable": {"thread_id": "math-thread"}}
    run_interaction("quanto fa 3 + 7?", config_math)
    run_interaction("e ora 10 + 4?", config_math)

    # Secondo thread: motivazione
    config_motivation = {"configurable": {"thread_id": "motivation-thread"}}
    run_interaction("dammi una frase motivante", config_motivation)

