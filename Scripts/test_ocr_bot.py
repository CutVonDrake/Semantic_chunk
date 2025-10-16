#!/usr/bin/env python3
import sys
import json
import argparse
import re
import ollama

# Definisci qui il percorso dell'immagine
DEFAULT_IMAGE = "/storage/data_4T_b/andreacutuli/PROVA/images/test/burn_car.png"

import re

def parse_response_text(resp):
    # 1) tenta attributi diretti
    for attr in ("text", "content", "output"):
        val = getattr(resp, attr, None)
        if val:
            return _clean_text(val)

    # 2) choices (list/tuple)
    choices = getattr(resp, "choices", None)
    if choices and isinstance(choices, (list, tuple)) and len(choices) > 0:
        first = choices[0]
        if isinstance(first, dict):
            return _clean_text(first.get("text") or first.get("content") or "")
        return _clean_text(getattr(first, "text", None) or getattr(first, "content", None) or "")

    # 3) fallback: estrai response='...' o response="..." dalla stringa generale
    s = str(resp)
    m = re.search(r"response=(?:'|\")(?P<t>.*?)(?:'|\")(?:\s|$)", s, flags=re.DOTALL)
    if m:
        raw = m.group("t")
        return _clean_text(raw)

    # 4) fallback generico
    return _clean_text(s)

def _clean_text(s):
    if s is None:
        return ""
    # se l'input è bytes, decodifica
    if isinstance(s, (bytes, bytearray)):
        try:
            s = s.decode("utf-8")
        except Exception:
            s = s.decode(errors="ignore")
    # rimuovi leading/trailing whitespace
    s = s.strip()
    # sostituisci escape comuni (\n, \t, \') con i loro caratteri
    try:
        s = bytes(s, "utf-8").decode("unicode_escape")
    except Exception:
        # fallback: sostituzioni semplici
        s = s.replace("\\n", "\n").replace("\\t", "\t").replace("\\'", "'").replace('\\"', '"')
    # se la stringa è racchiusa da virgolette singole o doppie, togli
    if len(s) >= 2 and ((s[0] == s[-1]) and s[0] in ("'", '"')):
        s = s[1:-1].strip()
    # se la libreria include "response=" ancora presente, elimina il prefisso
    s = re.sub(r"^response\s*=\s*", "", s, flags=re.IGNORECASE).strip()
    return s
def describe_image(model_name, image_path, prompt=None):
    if prompt is None:
        prompt = (
            "You are an image safety inspector. Analyze the image carefully.\n\n"
            "1. First, describe in detail what is visible in the image (people, objects, actions, scene).\n"
            "2. Then check specifically for ANY of the following elements:\n"
            "   - Guns, knives, explosives, or any type of weapon\n"
            "   - Blood, injury, corpses, or visible wounds\n"
            "   - Physical aggression, fights, threats, or violent behavior\n"
            "   - Hostage situations, shootings, executions, military combat\n"
            "   - Police or military pointing weapons at people\n"
            "   - Self-harm or harm to others\n\n"
            "If ANY of these are present, you MUST include exactly this line at the end of your response:\n"
            "\"Warning: VIOLENCE\"\n\n"
            "If none of these are present, end your answer with:\n"
            "\"No violence detected\"\n\n"
            "Be objective, specific, and do not omit potential signs of violence."
        )

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    client = ollama.Client()
    resp = client.generate(model=model_name, prompt=prompt, images=[image_bytes])
    text = parse_response_text(resp)
    return {"model": model_name, "image_path": image_path, "analysis": text}

def main():
    parser = argparse.ArgumentParser(description="Smart agent: describe an image via Ollama vision model")
    parser.add_argument("--image", help="Path to image file (optional, fallbacks to DEFAULT_IMAGE)")
    parser.add_argument("--model", default="granite3.2-vision", help="Vision model name")
    parser.add_argument("--prompt", help="Custom prompt to send to the model")
    parser.add_argument("--output", help="Path to save JSON output (defaults to stdout)")
    args = parser.parse_args()

    image_path = args.image or DEFAULT_IMAGE

    try:
        result = describe_image(args.model, image_path, args.prompt)
    except TypeError:
        client = ollama.Client()
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        prompt_text = args.prompt or (
            "Describe the image in detail, list any visible text and its approximate location, "
            "and state whether the image contains illegal or compromising elements. Be concise."
        )
        resp = client.chat(model=args.model, messages=[{"role":"user","content":prompt_text}], images=[image_bytes])
        result = {"model": args.model, "image_path": image_path, "analysis": parse_response_text(resp)}

    out = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(out)
    else:
        print(out)

if __name__ == "__main__":
    main()