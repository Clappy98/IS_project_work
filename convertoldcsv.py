import pandas as pd
import numpy as np
from polls.models import *

'''
31 risposte per 13 performance per ogni csv
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


df_stem = pd.read_csv('datasetScientificBackgroundFINAL.csv', sep=';')
df_arts = pd.read_csv('datasetArtisticBackgroundFINAL.csv', sep=';')

durations = []
performances_names = []

# save the durations and create the names for the performances
for i in range(13):
    durations.append(df_stem['timeDuration'][i*31])
    performances_names.append(f"Perf_{i+1}")

# attributes are the same between the two datasets
df_stem_ans = df_stem.filter(regex='Evaluation').drop(['EvaluationChoreographyStoryTelling'], axis=1)
df_stem_attr = df_stem.drop(list(df_stem_ans), axis=1).drop(['timeDuration'], axis=1)

df_arts_ans = df_arts.filter(regex='Evaluation').drop(['EvaluationChoreographyStoryTelling'], axis=1)

# create 62 users
users = []
for i in range(62):
    u = User()
    u.save()
    users.append(u.pk)


questions = []
stemAnswers = []
for _, row in df_stem_ans.iterrows():
    for key, value in row.iteritems():
        questions.append(eval_to_questions_dict[key])
        stemAnswers.append(str(value))

attributes = []
values = []
for _, row in df_stem_attr.iterrows():
    for key, value in row.iteritems():
        attributes.append(key)
        values.append(str(value))

artAnswers = []
for _, row in df_arts_ans.iterrows():
    for _, value in row.iteritems():
        artAnswers.append(str(value))

# extending users and names lists to have 31 copies of each entry
extended_users = np.array([[user]*31 for user in users]).flatten()
extended_performances_names = np.array([[name]*31 for name in performances_names]).flatten()


# creating attributes csv
pd.DataFrame({
    'PerformanceName':extended_performances_names,
    'AttributeName':attributes,
    'Value':values
}).to_csv('attributes_values.csv')

# creating evaluation csv (contains data from two datasets)
pd.DataFrame({
    'UserID':extended_users + extended_users,
    'UserBg':['Stem' for _ in range(len(stemAnswers))] + ['Arts' for _ in range(len(artAnswers))],
    'PerformanceName':extended_performances_names + extended_performances_names,
    'Question':questions + questions,
    'Answer':stemAnswers + artAnswers
}).to_csv('preexisting_evaluations.csv')

# creating a performances csv
pd.DataFrame({
    'PerformanceName':performances_names,
    'Duration':durations,
    'Year':['2022' for _ in range(len(performances_names))],
    'Link':[None for _ in range(len(performances_names))]
}).to_csv('performances_2022.csv')