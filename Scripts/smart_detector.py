import ollama
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END

# --- 1. Definizione dello Strumento (Tool) ---
# Incapsuliamo la tua logica di analisi dell'immagine in una funzione.
# Questo è lo "strumento" che l'agente potrà decidere di usare.

def analyze_image_violence(image_path: str) -> str:
    """
    Analizza un'immagine da un percorso specificato per determinare se 
    contiene contenuti violenti o inappropriati.
    """
    try:
        # 🔧 Specifica il modello che hai già scaricato
        model = "granite3.2-vision" # Assicurati che questo modello sia disponibile in locale

        # 🧠 Prompt specifico per l'analisi
        prompt = "Describe the contents of this image and determine whether it contains anything that might be legally or ethically inappropriate, violent, or adult-only content. Respond with a clear 'Violent' or 'Not Violent' classification, followed by a brief explanation."

        # 📤 Esegui inferenza con Ollama
        response = ollama.generate(
            model=model,
            prompt=prompt,
            images=[image_path]
        )
        
        return response['response']

    except Exception as e:
        return f"An error occurred: {str(e)}"

# --- 2. Definizione dello Stato dell'Agente ---
# Lo "stato" è la memoria del nostro agente. Mantiene traccia dei messaggi
# scambiati (input, output, chiamate a strumenti).

class AgentState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]

# --- 3. Creazione dei Nodi del Grafo ---
# I nodi sono le azioni che l'agente può compiere.

# Nodo 1: L'agente decide quale strumento usare (o se rispondere direttamente)
def agent_node(state):
    # Per questo semplice caso, assumiamo che l'utente voglia sempre analizzare un'immagine.
    # In un agente complesso, qui ci sarebbe un modello LLM che decide quale strumento usare.
    last_message = state['messages'][-1]
    
    # Eseguiamo direttamente lo strumento con il percorso dell'immagine dall'input
    result = analyze_image_violence(last_message.content)
    
    # Aggiungiamo il risultato allo stato per il prossimo passo
    return {"messages": [HumanMessage(content=result)]}

# Nodo 2: Il router decide se il lavoro è finito
def router_node(state):
    # In questo caso semplice, dopo aver chiamato lo strumento, il lavoro è sempre finito.
    return END

# --- 4. Costruzione del Grafo (Workflow) ---
# Definiamo il flusso di lavoro: come l'agente si muove tra i nodi.

workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END) # Semplice: agent -> fine

# Compiliamo il grafo per renderlo eseguibile
app = workflow.compile()

# --- 5. Esecuzione dell'Agente ---
# Ora puoi interagire con l'agente.

# 📂 Percorso dell'immagine
image_path = "/storage/data_4T_b/andreacutuli/PROVA/images/cats/zombie.jpg"

# 🗣️ Invia il messaggio all'agente (il contenuto è il percorso dell'immagine)
# L'input deve essere una lista di messaggi.
final_state = app.invoke({"messages": [HumanMessage(content=image_path)]})

# 📄 Estrai e stampa la risposta finale
final_response = final_state['messages'][-1].content
print("--- Analisi dell'Agente ---")
print(final_response)