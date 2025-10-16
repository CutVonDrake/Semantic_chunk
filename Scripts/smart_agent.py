#!/usr/bin/env python3
import os
import re
from dotenv import load_dotenv
load_dotenv()

# Pulizia chiavi vuote
if "MISTRAL_API_KEY" in os.environ and os.environ["MISTRAL_API_KEY"].strip() == "":
    os.environ.pop("MISTRAL_API_KEY", None)

LOCAL_LLM = os.environ.get("LOCAL_LLM", "granite4:latest")

from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langgraph.checkpoint.memory import InMemorySaver
import ollama

# --- Tool di analisi immagini ---
DEFAULT_IMAGE = "/storage/data_4T_b/andreacutuli/PROVA/images/test/burn_car.png"

def analyze_image(image_path: str = None) -> str:
    """Analizza un'immagine e rileva eventuale violenza"""
    image_path = image_path or DEFAULT_IMAGE
    model_name = "granite4-vision"  # o LOCAL_LLM se vuoi

    prompt = (
        "You are an image safety inspector. Analyze the image carefully.\n\n"
        "1. Describe in detail what is visible in the image (people, objects, actions, scene).\n"
        "2. Check for guns, knives, blood, physical aggression, hostages, self-harm.\n"
        "End with exactly one line: 'Warning: VIOLENCE' if any violent element is present, "
        "otherwise 'No violence detected'."
    )

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    client = ollama.Client()
    resp = client.generate(model=model_name, prompt=prompt, images=[image_bytes])

    def parse_text(resp):
        for attr in ("text", "content", "output"):
            val = getattr(resp, attr, None)
            if val:
                return str(val).strip()
        choices = getattr(resp, "choices", None)
        if choices:
            first = choices[0]
            if isinstance(first, dict):
                return first.get("text") or first.get("content") or ""
            return getattr(first, "text", None) or getattr(first, "content", None) or ""
        return str(resp).strip()

    return parse_text(resp)

# --- Modello ---
model = ChatOllama(model=LOCAL_LLM, temperature=0, max_tokens=150)

# Tool matematico di Morty
def add(a: int, b: int) -> int:
    return a + b

# --- Agenti ---
morty_agent = create_react_agent(
    model=model,
    tools=[add],
    prompt="You are Morty. You're a bit nervous. You handle math if Rick tells you to. After solving, go back to Rick.",
    name="Morty",
)

meeseeks_agent = create_react_agent(
    model=model,
    tools=[analyze_image],
    prompt=(
        "You are Mr. Meeseeks! You help with motivation, explanations, "
        "and image analysis if asked. After helping, return to Rick."
    ),
    name="MrMeeseeks",
)

# --- Supervisore Rick ---
rick_agent = create_supervisor(
    [morty_agent, meeseeks_agent],
    model=model,
    prompt=(
        "You are Rick Sanchez. You're the boss. You get all user requests.\n"
        "Decide who to send things to:\n"
        "- Morty if it's a math problem\n"
        "- Meeseeks if it's about help, motivation, or image analysis\n"
        "After they answer, return to the user with a sarcastic comment or summary."
    ),
    supervisor_name="Rick"
)

# --- Checkpoint ---
checkpointer = InMemorySaver()
app = rick_agent.compile(checkpointer=checkpointer)

# --- Cleaner output ---
TRANSFER_PATTERN = re.compile(r'\[\s*\{.*?\}\s*\]', re.DOTALL)

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
    msgs = turn.get("messages", [])
    for m in msgs:
        content = getattr(m, "content", None) or (m.get("content") if isinstance(m, dict) else None)
        name = getattr(m, "name", None) or (m.get("name") if isinstance(m, dict) else None) or getattr(m, "model", None) or "Agent"
        role = getattr(m, "role", None) or (m.get("role") if isinstance(m, dict) else None) or ""
        if isinstance(role, str) and role.lower().startswith("human"):
            continue
        raw = content if isinstance(content, str) else str(content)
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

# --- Funzione per interazione ---
def run_interaction(user_input, config=None):
    if config is None:
        config = {"configurable": {"thread_id": "default-thread"}}
    turn = app.invoke({"messages": [{"role": "user", "content": user_input}]}, config)
    print_messages(turn)
    return turn, config

# --- Esempi ---
if __name__ == "__main__":
    config_math = {"configurable": {"thread_id": "math-thread"}}
    run_interaction("quanto fa 3 + 7?", config_math)
    run_interaction("e ora 10 + 4?", config_math)

    config_motivation = {"configurable": {"thread_id": "motivation-thread"}}
    run_interaction("dammi una frase motivante", config_motivation)
    run_interaction(f"analizza immagine {DEFAULT_IMAGE}", config_motivation)
