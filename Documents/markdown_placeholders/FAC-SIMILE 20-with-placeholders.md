[[IMAGE-1]]

PROGETTO DI OTTIMIZZAZIONE DEL DISPATCHING PRODUTTIVO

Implementazione di un framework dinamico per il dispatching di ordini in ambiente produttivo tessile

FilTess Industria Tessile S.p.A.

Partner Tecnico:

OptiWare Consulting S.r.l.

[[TABLE-1]]

Introduzione

Il  presente  documento  rappresenta  il  deliverable  tecnico  finale  relativo  al  progetto  di ottimizzazione delle attività di dispatching presso gli impianti produttivi dell'azienda [Nome Azienda Tessile], operante nel settore della produzione tessile industriale. Il progetto è stato commissionato con l'obiettivo di analizzare, ridisegnare e ottimizzare il sistema di assegnazione e sequenziamento degli ordini di lavorazione, in modo da migliorare l'efficienza globale del sistema produttivo e ridurre i tempi di attraversamento dei lotti.

La crescente domanda di flessibilità produttiva e l'esigenza di mantenere alti livelli di qualità e puntualità  nelle  consegne  hanno  evidenziato  la  necessità  di  un  intervento  strutturato  sul sistema di gestione operativa delle risorse di produzione. In questo contesto, il dispatching -ovvero il processo decisionale che stabilisce quali ordini vanno lavorati, in quale sequenza e su quali macchine -rappresenta un punto critico su cui agire per ottenere benefici concreti in termini di produttività.

L'attività è stata svolta da [Nome Società di Consulenza], in qualità di partner consulenziale, con  il  coinvolgimento  diretto  del  team  tecnico  e  produttivo  di  [Nome  Azienda  Tessile].  La metodologia  adottata  ha  previsto  un  approccio  basato  sull'analisi  dei dati  storici,  sulla modellazione dei flussi produttivi e sulla validazione di scenari simulativi, al fine di identificare strategie di dispatching più efficaci e coerenti con i vincoli reali della produzione tessile.

Il  documento  fornisce  una  descrizione  dettagliata  del  contesto  iniziale,  degli  obiettivi perseguiti, delle soluzioni sviluppate, dei risultati ottenuti in termini quantitativi e qualitativi, e di un'analisi dei costi sostenuti in relazione ai benefici gene rati. Le sezioni seguenti seguiranno una struttura coerente con gli standard di rendicontazione tecnica e saranno supportate da tabelle, grafici e indicatori di performance  per  facilitare la lettura e la valutazione dell'intervento.

Descrizione del Problema e Obiettivi Tecnici

1. Contesto operativo e criticità iniziali

Il  sistema  produttivo  di  [Nome  Azienda  Tessile]  è  organizzato  su  più  linee  di  lavorazione parallele, ognuna delle quali può eseguire operazioni su diversi tipi di tessuti con differenti vincoli tecnologici e produttivi. La sequenza con cui i lotti di produzione vengono assegnati alle macchine influisce significativamente sull'efficienza complessiva del sistema, sui tempi di consegna e sull'utilizzo delle risorse. In assenza di una logica strutturata per il dispatching, l'azienda ha riscontrato negli anni le seguenti criticità:

● Eccessivo accumulo di work-in-progress (WIP) in prossimità di alcune macchine;

● Tempi di setup non ottimizzati, dovuti a passaggi frequenti tra lotti con caratteristiche molto diverse;

● Scarsa  visibilità  sullo  stato  di  avanzamento  degli  ordini  e  bassa  tracciabilità  delle decisioni di assegnazione;

● Utilizzo non bilanciato delle risorse disponibili;

● Difficoltà nel rispondere a variazioni impreviste nella domanda o nella disponibilità di macchinari.

2. Obiettivi tecnici del progetto

Alla luce delle criticità osservate, il progetto ha definito i seguenti obiettivi tecnici principali:

● Sviluppare  un  modello  formalizzato  del sistema  di dispatching esistente,  con l'identificazione dei colli di bottiglia e delle principali fonti di inefficienza;

● Introdurre  una  logica  decisionale  di  assegnazione  degli  ordini  basata  su  algoritmi ottimizzati (priorità dinamiche, regole composite, modelli stocastici);

● Ridurre i tempi medi di attraversamento (makespan) dei lotti;

● Abbattere  il  numero  di  cambi  formato  non  necessari  attraverso  una  strategia  di raggruppamento ottimale;

● Migliorare l'equilibrio del carico di lavoro tra le diverse linee di produzione;

● Abilitare la simulazione di scenari alternativi per supportare la pianificazione a medio termine.

3. Mappa sintetica degli obiettivi

[[TABLE-2]]

[[TABLE-3]]

Le prossime  sezioni descriveranno l'approccio metodologico adottato e le soluzioni algoritmiche sperimentate per il raggiungimento di tali obiettivi.

Approccio Metodologico e Soluzioni Sviluppate

1. Metodologia adottata

Il progetto è stato strutturato secondo una metodologia incrementale, basata sul ciclo 'analisi -modellazione -simulazione -validazione'. In una prima fase è stata effettuata una raccolta dati quantitativa e qualitativa, attraverso l'estrazione di log d i produzione dal MES aziendale, interviste con i responsabili di reparto e osservazioni dirette in linea. Sono stati classificati oltre 1200 lotti produttivi, registrando per ciascuno caratteristiche come tipo di tessuto, lavorazione richiesta, durata stimata, macchinari abilitati, e sequenze effettivamente eseguite.

In seguito, è stato realizzato un modello descrittivo del processo di dispatching, implementato in ambiente Python tramite una libreria custom basata su NetworkX e SimPy. Questo modello ha permesso di riprodurre digitalmente il comportamento delle linee, con possibilità di iniettare regole alternative di assegnazione e verificare i risultati tramite simulazione discreta.

2. Regole di dispatching sperimentate

Sono state testate sei regole di dispatching, suddivise tra approcci classici (statici) e avanzati (dinamici). Nello specifico:

● FIFO (First In First Out)

● SPT (Shortest Processing Time)

● LPT (Longest Processing Time)

● COVERT (minimizzazione latenze pesate)

● ATC (Apparent Tardiness Cost)

● RuleMix (approccio composito con ponderazione dinamica su più metriche)

Ogni regola è stata testata su 4 scenari di carico (basso, medio, alto, perturbato) e confrontata con i dati reali di produzione.

3. Soluzioni selezionate e architettura finale

L'analisi  dei  risultati  ha  mostrato  che  l'approccio  RuleMix  ha  garantito,  in  media,  i  migliori risultati in termini di riduzione dei tempi medi e della varianza nei lead time. È stato quindi

definito  un  framework  di  dispatching  dinamico  che,  a  ogni  ciclo  di  decisione,  calcola  un punteggio composito per ogni ordine, sulla base di:

● Urgenza rispetto alla data di consegna;

● Durata prevista della lavorazione;

● Cambi formato richiesti sulla macchina target;

● Priorità commerciale dell'ordine.

I punteggi vengono aggiornati ogni 15 minuti e la sequenza ottimale è generata in tempo reale tramite  una  funzione  obiettivo  multicriterio.  L'integrazione  con  il  sistema  MES  è  avvenuta attraverso  l'export  automatico  delle  sequenze  in  formato  XML,  con  poss ibilità  di  override manuale da parte dell'operatore.

Di seguito si riporta una tabella comparativa delle performance ottenute con le varie regole:

[[TABLE-4]]

La  soluzione  proposta  è  stata  validata  anche  tramite  stress  test  su  flussi  perturbati, confermando la maggiore robustezza dell'approccio dinamico rispetto ai metodi statici.

Risultati Raggiunti e Analisi dei Benefici

1. Valutazione delle Performance

A seguito della fase di validazione, il nuovo sistema di dispatching dinamico basato su RuleMix è  stato  progressivamente  introdotto  nella  pianificazione  quotidiana  dell'impianto  tessile. L'adozione di questa soluzione ha comportato un miglioramento misurab ile  delle  principali metriche  operative,  monitorate  per  10  settimane  consecutive  a  partire  dalla  messa  in esercizio.

I principali benefici osservati sono stati:

● Riduzione del makespan medio giornaliero da 192 a 163 minuti (-15,1%);

● Aumento dell'utilizzo medio delle risorse produttive dal 72,8% all'83,5%;

● Calo del numero medio di cambi formato per turno da 9,6 a 7,4 (-23,1%);

● Diminuzione  della  varianza  nei  lead  time  di  produzione  (indicatore  di  stabilità  del flusso);

● Incremento della puntualità nelle consegne (ontime delivery) dal 78% all'89%.

Questi dati sono stati raccolti tramite un modulo di monitoraggio integrato al MES e validati dal team qualità.

2. Analisi dei Benefici Qualitativi

Oltre ai miglioramenti quantitativi, il nuovo sistema ha prodotto benefici qualitativi rilevanti:

● Maggiore affidabilità del piano di produzione settimanale, grazie alla riduzione degli imprevisti;

● Aumento  della  trasparenza  delle  decisioni  operative,  supportata  da  dashboard interattive a disposizione dei responsabili di reparto;

● Miglior collaborazione tra pianificazione centrale e operatori di linea, attraverso logiche più comprensibili e adattive;

● Capacità di risposta più rapida in caso di guasti o riassegnazione urgente di ordini ad altre macchine.

di Dispatching: Makespan

[[IMAGE-2]]

Questi elementi hanno favorito un generale miglioramento della governance della produzione e della cultura del dato tra i team coinvolti.

3. Confronto con Obiettivi Iniziali

La tabella seguente mostra un confronto sintetico tra i target definiti in fase progettuale e i risultati effettivamente raggiunti:

[[TABLE-5]]

[[TABLE-6]]

In  sintesi,  i  risultati  ottenuti  hanno  soddisfatto  e  in  alcuni  casi  superato  le  attese,  con scostamenti limitati e pienamente giustificabili alla luce delle dinamiche reali dell'impianto.

Makespan

[[IMAGE-3]]

Analisi dei Costi e Ritorno sull'Investimento (ROI)

1. Costi sostenuti per il progetto

Il progetto ha comportato un investimento distribuito su diverse voci, riconducibili sia a costi diretti che indiretti. Nella tabella seguente è riportata una sintesi dei principali costi sostenuti durante l'intero ciclo di vita del progetto:

[[TABLE-7]]

[[TABLE-8]]

2. Benefici economici annui stimati

Sulla base dei risultati ottenuti, sono stati stimati i seguenti benefici economici su base annua:

● Riduzione del costo uomomacchina per effetto dell'aumento di produttività: € 36.000

● Riduzione dei costi legati a ritardi di consegna (penali e rientri): € 14.500

● Risparmio per minori fermi macchina e ottimizzazione setup: € 11.000

● Riduzione di scarti e rilavorazioni grazie a maggiore stabilità dei flussi: € 4.000

Totale benefici annui stimati: € 65.500

3. ROI e Break-even

Il ritorno sull'investimento è stato calcolato secondo la formula:

``` ROI = (Benefici Annui - Costo Totale) / Costo Totale ```

Applicando i valori raccolti:

` ROI = (65.500 - 50.000) / 50.000 = 31% `

Il  tempo  stimato  per  raggiungere  il  break-even  è  pari  a 9,2  mesi ,  tenendo  conto  di  una distribuzione progressiva dei benefici a partire dal terzo mese post-deployment.

[[IMAGE-4]]

L'analisi economica  del  progetto  non  solo  ha confermato  la sostenibilità finanziaria dell'intervento, ma ha anche evidenziato un ampio margine di ritorno nel medio periodo. Il raggiungimento del  break-even  in meno  di  dieci  mesi  rappresenta  un  indicatore  chiave  di successo, soprattutto in un settore manifatturiero come  quello tessile, storicamente caratterizzato da margini operativi compressi e cicli produttivi soggetti a forte stagionalità.

Inoltre, l'approccio incrementale e data -driven adottato si è dimostrato efficace nel ridurre il rischio di interruzioni operative, favorendo un processo di adozione graduale ma strutturato. I miglioramenti  rilevati,  sia  a  livello  operativo  che  qualitativo,  hanno  superato  le  aspettative iniziali e offerto uno stimolo per un'estensione futura del modello ad altre aree della supply chain aziendale.

In prospettiva, il progetto può essere considerato una best practice di riferimento per interventi futuri orientati alla digitalizzazione, alla riduzione degli sprechi e all'agilità decisionale nella pianificazione. Il framework sviluppato è tecnicamente scalabile, economicamente sostenibile e perfettamente allineato con gli obiettivi strategici di competitività e resilienza a lungo termine dell'azienda.

Riferimenti

1. Herrmann, J.W., & Lee, H. (2021). 'Dispatching Rules in Manufacturing Systems: A Review  of  Advances  and  Industrial  Practices.' International  Journal  of  Production Research , 59(10), 3052 -3071.

2. Slack, N., Brandon-Jones, A., & Johnston, R. (2022). Operations Management (10th ed.). Pearson Education.

3. Siemens Digital Industries (2023). 'Advanced Scheduling and Dispatching: A Smart Approach to Improve Shop Floor Execution.' Whitepaper.

4. Geng, Z., & Chu, C. (2020). 'Multi -criteria dynamic dispatching in hybrid flow shop with realtime disturbances.' Computers & Industrial Engineering , 142, 106344.

5. UNI EN ISO 224002:2014. 'Indicatori di prestazione per la gestione della produzione.'

6. IBM  Supply  Chain  Solutions  (2022).  'From  Static  Planning  to  Smart  Scheduling: Enabling Agile Operations in Manufacturing.' Technical Brief.
