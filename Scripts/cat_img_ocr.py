import ollama

# 🔧 Specifica il modello che hai già scaricato
model = "granite3.2-vision"

# 🧠 Prompt testuale
prompt = "Describe the contents of this image and determine whether it contains anything that might be legally or ethically inappropriate."



# 📂 Percorso dell'immagine
image_path = "/storage/data_4T_b/andreacutuli/PROVA/images/cats/zombie.jpg"

# 📤 Esegui inferenza
response = ollama.generate(
    model=model,
    prompt=prompt,
    images=[image_path]
)

print(response['response'])
