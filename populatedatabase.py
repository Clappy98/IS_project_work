import pandas as pd
import sys
import getopt
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testsite.settings")
django.setup()

import polls.models as models

# header = PerformanceName - Duration - Year - Link
def insert_performances(filename, sep):
    df = pd.read_csv(filename, sep=sep)

    for row in df.itertuples():
        models.Performance.objects.get_or_create(
            name=row.PerformanceName,
            year=row.Year,
            duration=row.Duration,
            link=row.Link
        )


# header = QuestionCategory - QuestionText - QuestionPhrasing
def insert_questions_and_categories(filename, sep):  
    df = pd.read_csv(filename, sep=sep)

    '''
    Used get_or_create() method to ensure that
    no duplicate objects are created everytime
    the script is executed. This ensure to get
    the question category and, if not already
    seen, to insert it in the database at the
    same time
    '''

    # insert questions and create relationship
    for row in df.itertuples():
        q, _ = models.Question.objects.get_or_create(
            text=row.QuestionText,
            is_negative=True if row.QuestionPhrasing=="P" else False
        )

        c, _ = models.Category.objects.get_or_create(pk=row.QuestionCategory)

        models.QuestionCategory.objects.get_or_create(
            question=q,
            category=c
        )


''' Performances should already exist, must find a solution '''
# header = PerformanceName - AttributeName - Value
def insert_attributes(filename, sep):
    df = pd.read_csv(filename, sep=sep)

    for row in df.itertuples():
        p = models.Performance.objects.get(pk=row.PerformanceName)

        a, _ = models.Attribute.objects.get_or_create(
                name=row.AttributeName,
        )

        models.PerformanceCharacteristic.objects.get_or_create(
            performance=p,
            attribute=a,
            value=str(row.Value)
        )


''' Performances should already exist, must find a solution '''
''' Questions should already exist, must find a solution '''
# header = UserID - UserBg - PerformanceName - Question - Answer
def load_preexisting_evaluation(filename, sep):
    df = pd.read_csv(filename, sep=sep)

    for row in df.itertuples():
        u, _ = models.User.objects.get_or_create(pk=row.UserID)
        bg, _ = models.Background.objects.get_or_create(pk=row.UserBg)

        # add relation
        models.Experience.objects.get_or_create(
            user=u,
            background=bg
        )

        p = models.Performance.objects.get(pk=row.PerformanceName)
        q = models.Question.objects.get(pk=row.Question)

        # add answer
        models.Answer.objects.get_or_create(
            user=u,
            performance=p,
            question=q,
            value=row.Value
        )




'''
Script starts here
'''
opts, args = getopt.getopt(
    sys.argv[1:],
    '',
    longopts=[
        'Questions_and_categories_csv=',
        'Attribute_csv=',
        'Performance_csv=',
        'Preexisting_eval_csv='
    ]
)

# opt = (arg, val)
for opt in opts:
    if(opt[1] == ''):
        raise ValueError(f"Specify a csv to load for <{opt[0]}>")
    
    elif(opt[0] == '--Questions_and_categories_csv'):
        print(f"Loading questions and categories from <{opt[1]}>")

        insert_questions_and_categories(
            filename=opt[1],
            sep=';'
        )

        print(f"Loaded questions and categories")

    elif(opt[0] == '--Attribute_csv'):
        print(f"Loading attributes from <{opt[1]}>")

        insert_attributes(
            filename=opt[1], 
            sep=';'
        )

        print(f"Loaded attributes")

    elif(opt[0] == '--Performance_csv'):
        print(f'Loading performance from {opt[1]}')

        insert_performances(
            filename=opt[1],
            sep=';'
        )

        print(f'Loaded performances')

    elif(opt[0] == '--Preexisting_eval_csv'):
        print(f"Loading evaluations from <{opt[1]}>")

        load_preexisting_evaluation(
            filename=opt[1],
            sep=';'
        )

        print(f"Loaded evaluations")

    else:
        raise ValueError(f"<{opt[0]}> is not a supported argument")