## Prerequisiti
L'applicazione ha bisogno dei seguenti package Python per funzionare:
- `Django`
- `NumPy`
- `Pandas`

## Database
### Settings
Per settare il database da utilizzare:
1. Creare un file `database.conf`
2. All'interno del file specificare il database da utilizzare utilizzando la seguende sintassi:<br>
`DATABASE(engine, databaseName, username, password, host, port)`
    - `engine` : il database backend da utilizzare, consultare la [documentazione](https://docs.djangoproject.com/en/4.0/topics/install/#database-installation) per ulteriori informazioni. Al momento è stato testato il funzionamento solo con [PostgreSQL](https://www.postgresql.org/);
    - `databasename` : il nome del database da utilizzare. Assicurarsi di aver creato il database prima di procedere;
    - `username` : l'utente con cui l'applicazione andrà a svolgere le operazioni sul database;
    - `password` : la password da usare per connettersi al database;
    - `host` : che host usare per connettersi al database;
    - `port` : che porta usare per connettersi al database;
**N.B. Gli spazi bianchi dopo le virgole per il momento sono obbligatori**

### Schema
Di seguito il [diagramma](./dbschema.svg) che rappresenta le tavole del database e le loro relazioni:
![database schema](dbschema.svg)

## Sito
### Mappa del sito
Di seguito lo [schema](./sitemap.svg) rappresentante la mappa del sito, un possibile design delle schede, il nome della vista (in [views.py](./polls/views.py)) e del template (in [template/polls](./polls/templates/polls/)) associati alla singola scheda:
![site map](sitemap.svg)

### Viste
Di seguito verranno elencate le funzionalità delle viste implementate:
- `homepage()` : renderizza la homepage del sito;
- `prepareUser()` : genera un User da utilizzare successivamente;
- `selectBackground(user)` : renderizza la pagina di scelta del background dell'user;
- `manageBackgroundSelection(user)` : registra la scelta del background;
- `prepareQuestionnaire(user)` : sceglie una performance casuale da cui iniziare il questionario;
- `showQuestionnaire(user, performance)` : renderizza la pagina mostrante il questionario per una certa performance;
- `manageQuestionnaireAnswer(user, performance)` : registra le risposte date dall'user relative alla performance mostrata. Se l'utente ha compilato il questionario per tutte le performance disponibili, verrà indirizzato alla homepage, altrimenti verrà scelta una nuova performance;

## Scripts
### convertoldcsv.py
Questo script converte i dataset pre-esistenti (`datasetScientificBackgroundFINAL.csv` e `datasetArtisticBackgroundFINAL.csv`) in nuovi dataset con una forma utile per essere salvati nel database.
In particolare, saranno creati i seguenti csv con i relativi header:
- `preexisting_evaluations.csv`, header = `UserID | UserBg | PerformanceName | Question | Answer`;
    - contiene le risposte di ogni utente per ogni domanda;
    - non essendo possibile ricavare dai vecchi dataset a quale performance fosse associata ogni risposta, è stato scelto di creare delle performance dummy (con nome 'Perf_i') a cui associare queste risposte;
    - dovendo associare anche degli utenti ad ogni risposta, vengono creati tanti utenti dummy quanti sono gli utenti che hanno risposto al vecchio questionario;
- `attributes_values.csv`, header = `PerformanceName | AttributeName | Value`;
    - per attributi si intendono le features
- `performances_2022.csv`, header = `PerformanceName | Duration | Year | Link`;
    - `Link` sarà una colonna di valori nulli;

Questo script va eseguito nella stessa cartella in cui sono presenti i dataset degli anni passati.

### populatedatabase.py
Questo script serve per popolare il database utilizzando dei csv. Lo script accetta i seguenti argomenti:
- `Question_and_categories_csv`: nome del csv contenente i testi e le categorie delle domande da inserire;
    - header atteso = `QuestionCategory | QuestionText | QuestionPhrasing`;
    - è già stato reso disponibile un [file](./questions.csv) da usare come paramentro per questo argomento;
- `Attribute_csv`: nome del csv contenente i valori assegnati alle features di ogni performance;
    - header atteso = `PerformanceName | AttributeName | Value`;
    - questo argomento **deve** essere inserito solo dopo aver caricato il file con le performance;
- `Performance_csv`: nome del csv contenente i dati sulle performances;
    - header atteso = `PerformanceName | Duration | Year | Link`;
- `Preexisting_eval_csv`: nome del csv contenente le risposte al questionario degli anni passati;
    - header atteso = `UserID | UserBg | PerformanceName | Question | Answer`;
    - questo argomento **deve** essere inserito solo dopo aver caricato il file con le performance e il file con le domande;

Esempio di chiamata a questo script:<br>
`py populatedatabase.py --Performance_csv=perf.csv --Attribute_csv=attribute.csv`

## Utilizzo
Per testare l'applicazione, spostarsi con il terminale all'interno della cartella contenente il file `manage.py` ed eseguire i seguenti comandi:
1. `py manage.py makemigrations polls`;
2. `py manage.py migrate`;
3. `py manage.py runserver`;

I passi **1.** e **2.** sono necessari solo alla prima esecuzione e ogniqualvolta vengano effettuate modifiche ai modelli del database.<br>
**N.B. Assicurarsi di aver creato il database che si intente utilizzare prima di testare l'applicazione**
