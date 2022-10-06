import pandas as pd
import numpy as np

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testsite.settings")
django.setup()

from polls.models import *

'''
31 risposte per N_QUESTIONS per 13 performance per ogni csv
nei vecchi csv non è presente a che performance è dedicata
ogni risposta, quindi verranno chiamate Perf_1,...,Perf_13
'''

eval_to_questions_dict = {
    'EvaluationChoreographyMovementTechnique':'The transition between one pose and the next are smooth and not forced',
    'EvaluationChoreographyRhythm':'The choreography links well with the music and the rhythm',
    'EvaluationChoreographyHumanCharacterization':'The movements performed during the choreography are so natural that resemble human ones',
    'EvaluationChoreographySpace':'The intepreter makes a satisfying use of the space',
    'EvaluationHumanReproducibility':'A human dancer would be able to easily reproduce the choreography',
    'EvaluationPublicInvolvement':'The interpreter is able to involve the public'
}

# I LINK A GITHUB DEVONO ESSERE AL RAW CONTENT MANNAGGIA A QUEL PORCO DI DIO
df_stem = pd.read_csv('https://raw.githubusercontent.com/ProjectsAI/NAOPlanningChallenge/main/datasets/datasetArtisticBackgroundFINAL.csv', sep=';')
df_arts = pd.read_csv('https://raw.githubusercontent.com/ProjectsAI/NAOPlanningChallenge/main/datasets/datasetScientificBackgroundFINAL.csv', sep=';')

print(
"+--------------------------------+\n\
| DATASET CARICATI               |\n\
+--------------------------------+"
)


durations = []
performances_names = []

# save the durations and create the names for the performances
for i in range(13):
    durations.append(df_stem['timeDuration'][i*31])
    performances_names.append(f"Perf_{i+1}")

# attributes are the same between the two datasets
# interessano le risposte date alle varie categorie, story telling non è contemplata nel nuovo questionario
df_stem_ans = df_stem.filter(regex='Evaluation').drop(['EvaluationChoreographyStoryTelling'], axis=1)
df_arts_ans = df_arts.filter(regex='Evaluation').drop(['EvaluationChoreographyStoryTelling'], axis=1)

# una volta ottenute le colonne delle risposte, le droppiamo insieme alla durata per estrarre soltanto gli attributi
df_attr = df_stem.drop(list(df_stem_ans), axis=1).drop(['timeDuration'], axis=1).drop(['EvaluationChoreographyStoryTelling'], axis=1)


# create 62 users (31 stem + 31 arts)
users = []
for i in range(62):
    u = User()
    u.save()
    users.append(u.pk)


answeredQuestions = []      # len = n_quest * n_users * n_perf
stemAnswers = []            # len = n_quest * n_users/2 * n_perf
# per ogni riga, si salva che risposta è stata data ad una certa domanda
for _, row in df_stem_ans.iterrows():
    for key, value in row.iteritems():
        answeredQuestions.append(eval_to_questions_dict[key])   # contiene duplicati
        stemAnswers.append(str(value))

artAnswers = []     # len = n_quest * n_users/2 * n_perf
for _, row in df_arts_ans.iterrows():
    for key, value in row.iteritems():
        answeredQuestions.append(eval_to_questions_dict[key])
        artAnswers.append(str(value))


# ne va salvata una sola copia ogni 31 righe (gli attributi di una performance sono copiati per 31 righe)
attributes = []     # len = n_attr * n_perf
values = []         # len = n_attr * n_perf
i=0
# per ogni riga si salva che valore è stato attribuito ad un certo attributo
for _, row in df_attr.iterrows():
    if i==0:
        for key, value in row.iteritems():
            attributes.append(key)  # contiene duplicati
            values.append(str(value))
    i = (i+1) % 31  # questo dovrebbe impedire che si salvino 31 copie di ogni attributo di una performance



# creating attributes csv
attributes_per_performance = int(len(attributes)/len(performances_names))    # indica quanti attributi sono presenti per ogni performance
print(f"attributes = {attributes_per_performance}")
pd.DataFrame({
    'PerformanceName':np.array([[name]*attributes_per_performance for name in performances_names]).flatten(),   # lista in cui il nome di una performance è ripetuto tante volte quanti sono il numero di attributi
    'AttributeName':attributes,
    'Value':values
}).to_csv('attributes_values.csv', index=False)


# nel csv ho risposte per ogni utente per ogni performance in quest'ordine  (P:U:Q --> ogni 6 Q, cambia U; ogni 31 U, cambia P)
# creating evaluation csv (contains data from two datasets)
answers_per_performance = int(len(answeredQuestions) / (len(performances_names)))    # indica quante domande sono state risposte per ogni performance    
answers_per_user_per_performance = int(answers_per_performance / len(users))         # indica a quante domande per ogni perfomance ha risposto ogni utente
print(f"answers per performance = {answers_per_performance}\nanswers per user per performance = {answers_per_user_per_performance}")
pd.DataFrame({
    'UserID': np.array([[user]*answers_per_user_per_performance for user in users]*len(performances_names)).flatten(),  # un array del tipo [(u1*n_quest, u2*n_quest, ...)*n_perf]                                                                                                                        
    'UserBg':['Stem' for _ in range(len(stemAnswers))] + ['Arts' for _ in range(len(artAnswers))],
    'PerformanceName': np.array([[perf]*answers_per_performance for perf in performances_names]).flatten(),             # un array del tipo [p1*n_quest*n_users, p2*n_quest*n_users, ...]
    'Question':answeredQuestions,
    'Answer':stemAnswers + artAnswers
}).to_csv('preexisting_evaluations.csv', index=False)

# creating a performances csv
pd.DataFrame({
    'PerformanceName':performances_names,
    'Duration':durations,
    'Year':['2022' for _ in range(len(performances_names))],
    'Link':[None for _ in range(len(performances_names))]
}).to_csv('performances_2022.csv', index=False)