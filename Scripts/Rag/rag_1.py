import torch

# Controlla se PyTorch è installato
print(f"PyTorch è installato. Versione: {torch.__version__}")

# Testa la creazione di un tensore
try:
    x = torch.rand(5, 3)
    print("Test di creazione del tensore riuscito:")
    print(x)
except Exception as e:
    print(f"Errore durante la creazione del tensore: {e}")

# (Opzionale) Controlla la disponibilità della GPU (CUDA)
if torch.cuda.is_available():
    print("\nSupporto GPU (CUDA) disponibile.")
    # Crea un tensore sulla GPU
    try:
        device = torch.device("cuda")
        y = torch.ones_like(x, device=device)
        x_cuda = x.to(device)
        z = x_cuda + y
        print("Test di calcolo su GPU riuscito:")
        print(z)
        print(f"Dispositivo del tensore z: {z.device}")
    except Exception as e:
        print(f"Errore durante il test della GPU: {e}")
else:
    print("\nSupporto GPU (CUDA) non disponibile. Verrà utilizzata la CPU.")