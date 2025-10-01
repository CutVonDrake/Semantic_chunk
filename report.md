# Report Dettagliato: Sviluppo di una Pipeline di Analisi Documentale Multimodale

## 1. Obiettivo del Progetto

L'obiettivo di questo progetto è sviluppare una pipeline robusta per l'estrazione e l'analisi di informazioni da documenti PDF. La pipeline deve essere in grado di gestire non solo il testo, ma anche elementi complessi come tabelle (incluse quelle che si estendono su più pagine), immagini e grafici, arricchendo infine il contenuto estratto con il riconoscimento di entità nominate (NER).

---

## 2. Estrazione di Testo e Tabelle: Strumenti a Confronto

La prima fase si è concentrata sulla conversione affidabile dei contenuti testuali e tabellari dei PDF.

### 🛠️ Tool 1: `Docling`

`Docling` è stato il primo strumento analizzato per la sua capacità di convertire PDF in Markdown.

#### Risultati dei Test
-   **Fac simile 2:** Riconosciuto come "Buono".
-   **Fac simile 5:** "Tutto perfetto" per quanto riguarda la struttura, ma è emerso un problema critico. Docling a volte toglie gli zeri dalle migliaia
-   **Fac simile 8:** Il testo è stato estratto in modo quasi corretto, ma la tabella, estesa su due pagine, non è stata riconosciuta.

#### 🐛 Problemi Identificati

1.  **Troncamento dei Numeri:**
    > **Problema:** `Docling` rimuove i punti usati come separatori delle migliaia, trasformando valori come "1.000" in "1". Questo comportamento è stato osservato nei *Fac simile 5* e *8* e rende i dati numerici inutilizzabili.
    >
    > **Tentativi di Soluzione:**
    > -   Modificare le impostazioni di `Docling`: **Nessun cambiamento**.
    > -   **Azione Definitiva:** È stata aperta una **issue su GitHub** per segnalare il bug al team di sviluppo, allegando screenshot.
    > -   **Workaround Efficace:** Modificando manualmente il PDF di test per rimuovere i punti dai numeri (es. "1000" invece di "1.000"), `Docling` ha estratto i valori correttamente. Questo suggerisce che un pre-processing del PDF potrebbe essere una soluzione temporanea.

2.  **Gestione di Tabelle Multi-pagina:**
    > **Problema:** Una tabella che si estende su due pagine nel *Fac simile 8* non è stata riconosciuta come un'unica entità. La parte sulla seconda pagina è stata completamente ignorata.

*Nota: Sono state effettuate prove anche con altri parser su Hugging Face (`unstructured`, `fast_pdf`), che non hanno risolto i problemi riscontrati.*

### 🛠️ Tool 2: `pdfPlumber`

Per confrontare i risultati, è stato testato anche `pdfPlumber`.

#### Risultati dei Test

-   **Problema dei Numeri:** `pdfPlumber` manifesta lo **stesso identico problema** di `Docling` con i separatori delle migliaia.
-   **Gestione Tabelle Multi-pagina:**
    > **Vantaggio Chiave:** A differenza di `Docling`, `pdfPlumber` ha dimostrato una gestione superiore delle tabelle multi-pagina nel *Fac simile 8*. Sebbene il layout non fosse perfettamente sincronizzato, le due parti della tabella sono state **"accorpate"** in un'unica struttura dati. Questo è un vantaggio significativo.

### 💡 Prova Aggiuntiva: Estrazione Separata di Testo e Tabelle

-   **Test con Fac simile 11:** È stato provato un approccio custom in cui testo e tabelle vengono estratti separatamente. Questo metodo ha prodotto un output in cui le tabelle appaiono "a cascata", una sotto l'altra.
-   **Confronto:** Questo approccio si è rivelato più efficace di `Docling` per il *Fac simile 8*, che non rilevava affatto la tabella nella seconda pagina.

---

## 3. Analisi della Struttura del Documento (Layout Recognition)

Per superare i limiti dei parser basati su testo, è stata esplorata l'analisi del layout visivo.

### 🖼️ Tool: `LayoutParser`

`LayoutParser` è stato scelto per la sua capacità di identificare la struttura logica di una pagina (blocchi di testo, immagini, tabelle, ecc.) dopo averla convertita in immagine.

#### Setup e Installazione

-   **Problema Locale:** Durante l'installazione su un ambiente Jupyter locale, si è verificato un errore persistente: `nonetype model`. L'ipotesi, supportata da ChatGPT, era che il modello di layout non venisse caricato correttamente.
-   **Causa Probabile:** La mancata installazione di `git` sull'ambiente locale impediva l'installazione corretta di `detectron2`, una delle dipendenze fondamentali di `LayoutParser`.
-   **✅ Soluzione:** L'installazione è stata spostata su **Google Colab**, dove è stato possibile installare tutte le dipendenze senza problemi.

#### Risultati del Test
> L'esperimento è stato un successo. Utilizzando uno screenshot di una pagina contenente sia testo che un'immagine (di "Yu-Gi-Oh!"), `LayoutParser` **ha correttamente segmentato e identificato i due blocchi distinti**.
>
> La documentazione di riferimento per l'implementazione è stata il seguente notebook su GitHub:
> `https://github.com/Layout-Parser/layout-parser/blob/main/examples/Deep%20Layout%20Parsing.ipynb`

---

## 4. Riconoscimento di Entità Nominate (NER)

Per arricchire semanticamente il testo estratto, è stato scelto un modello NER flessibile.

### ✨ Tool: `Gliner`

`Gliner` è stato selezionato per la sua capacità di funzionare con etichette personalizzate senza richiedere un addestramento estensivo.

#### Setup e Primi Test

-   **Ricerca Iniziale:** Dopo aver testato la demo online sul sito ufficiale e averne verificato l'efficacia, si è deciso di procedere con l'installazione locale.
-   **Problemi di Compatibilità:** L'installazione ha presentato diverse difficoltà. La causa è stata identificata in un'incompatibilità con la versione di Python in uso (probabilmente Python 13).
-   **✅ Soluzione:** È stato creato un **nuovo ambiente virtuale con Python 11**, che ha permesso di installare `Gliner` correttamente.
-   **Implementazione:** Un primo test su Jupyter, basato sull'esempio di Hugging Face, ha funzionato. Il parametro `threshold` per la confidenza delle predizioni è stato facilmente impostato (es. `threshold=0.4`) grazie a un esempio trovato su Colab.

#### Sfide e Prossimi Passi

1.  **Limite di Token:**
    > Un test su un documento completo ha generato un **warning di "lunghezza massima tokens raggiunta"**. Questo conferma la necessità di implementare una strategia di **chunking**, ovvero dividere il testo in porzioni più piccole prima di processarlo con `Gliner`.

2.  **Definizione delle Etichette:**
    > La sfida principale ora è definire un set di etichette abbastanza generico da essere applicabile a tutti i documenti. Le entità di interesse includono:
    > -   **Ragioni Sociali:** Trovare un modo per non separare entità come `s.r.l.` o `S.p.A.`.
    > -   **Strutture Documentali:** Identificare elementi come `Titoli` e `Paragrafi numerati` (es. "par 1.1").

---

## 5. Estrazione di Informazioni da Elementi Visivi (Immagini e Grafici)

Questa è stata l'area di ricerca più complessa, volta a "tradurre" immagini e grafici in testo.

### 🧪 Fase 1: Esplorazione di `SigLIP` e `SigLIP 2`

L'indagine è iniziata con `SigLIP`, un modello di visione-linguaggio di Google.

#### Sperimentazione
-   **Test su Colab:** Sono state testate sia la versione base che quella avanzata (con `BitsAndBytesConfig`), ma quest'ultima ha fallito con un `RuntimeError: self and mat2 must have the same dtype, but got Half and Byte`.
-   **Confronto SigLIP vs SigLIP 2:** `SigLIP 2` ha generalmente mostrato performance migliori, sebbene in alcuni casi isolati il primo `SigLIP` abbia dato risultati superiori (motivo da approfondire).
-   **Test Multilingua:** È stato osservato un calo di performance con l'italiano.
    -   `50.4%` that image 0 is 'une photo de 2 chats' (Francese)
    -   `41.3%` that image 0 is 'a photo of two cats' (Inglese)
    -   `38.7%` that image 0 is 'una foto di due gatti' (Italiano)

#### 🛑 Limitazione Fondamentale e Abbandono

> **Conclusione:** `SigLIP` **non è un modello generativo (captioner)**. È un encoder che crea embedding e li confronta con etichette di testo fornite. Non può generare una descrizione da zero. L'idea di usarlo per il captioning è stata **abbandonata ("mollato")**, poiché l'alternativa (passare i suoi embedding a un decoder come T5/GPT-2) richiederebbe un complesso processo di fine-tuning.

### 🧪 Fase 2: Valutazione di Altri Modelli di Captioning

-   **`BLIP`**: Testato brevemente, ha descritto correttamente un'immagine di un orso, ma è stato accantonato ("mollato, forse approfondire").
-   **`Microsoft GIT`**: Scartato.
-   **`MatCha`**: Identificato come una soluzione **estremamente promettente e matura**, in quanto pre-addestrato specificamente su grafici e diagrammi. Utilizza `Pix2Struct` come backbone. **Marcato come "da approfondire"**.

### ✅ Fase 3: Soluzione Adottata con `Ollama`

La svolta è arrivata con l'utilizzo di modelli multimodali open-source in locale tramite `Ollama`.

-   **Setup:** `Ollama` è stato installato per gestire e servire modelli LLM localmente.
-   **Modelli Testati:** `LLaVA` e `IBM Granite`.
-   **Risultati del Confronto:**
    > -   **Immagini Generiche:** Entrambi i modelli si sono comportati bene.
    > -   **Grafici e Diagrammi:** **`Granite` si è dimostrato nettamente superiore**, fornendo descrizioni più accurate, dettagliate e strutturate.

---

## 6. Definizione della Pipeline Operativa Finale

Sulla base di tutte le sperimentazioni, è stata progettata la seguente pipeline automatizzata:

1.  **Fase 1: Conversione e Placeholder**
    -   Uno script prende in input un file PDF.
    -   Il PDF viene convertito in Markdown usando **`Docling`**.
    -   Durante la conversione, lo script rileva immagini e tabelle:
        -   Le salva come file separati in una cartella (`./immagini_estratte`).
        -   Inserisce un **placeholder** univoco (es. `[IMMAGINE_01]`) nel file Markdown al posto dell'oggetto visivo.
    -   I file Markdown con i placeholder vengono salvati in un'altra cartella (`./markdown_con_placeholder`).

2.  **Fase 2: Analisi Visiva**
    -   Un secondo script itera su tutti i file nella cartella `./immagini_estratte`.
    -   Ogni immagine/tabella viene passata a **`Granite`** (servito tramite `Ollama`) per generare una descrizione testuale dettagliata (captioning/OCR).
    -   Tutte le descrizioni testuali vengono salvate in una cartella finale (`./descrizioni_testuali`).

3.  **Fase 3: Unione e Arricchimento (da implementare)**
    -   Un ultimo script leggerà i file Markdown, cercherà i placeholder e li sostituirà con le descrizioni testuali corrispondenti.
    -   Il testo completo verrà quindi diviso in **chunk semantici** (es. con `LangChain`).
    -   Infine, **`Gliner`** verrà applicato a ogni chunk per estrarre le entità nominate.

---

## 7. Riepilogo, Sfide Future e Note

### Riepilogo delle Scelte Tecnologiche
-   **Estrazione Testo/Tabelle:** `Docling` (con workaround per i numeri) o `pdfPlumber` (se le tabelle multi-pagina sono prioritarie).
-   **Analisi Layout:** `LayoutParser` (utile per validazione e estrazione di immagini).
-   **Image/Chart Captioning:** `Granite` via `Ollama` (soluzione vincente).
-   **NER:** `Gliner` (con necessità di chunking).

### Sfide Future da Affrontare
-   **NER su Chunk:** Sviluppare una logica per riunire entità che vengono spezzate dal processo di chunking (es. "S." in un chunk e "p.A." in quello successivo).
-   **Valutazione di `MatCha`:** Dedicare tempo a un test approfondito di `MatCha` per capire se offre performance superiori a `Granite` sui grafici tecnici.

### Appunti Tecnici
-   `windows deploted per liberare spazio cercare`
-   `Ram swap`