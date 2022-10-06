import pandas as pd
import sys
import getopt
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testsite.settings")
django.setup()

import polls.models as models
from django.db.models import Model
from django.db import IntegrityError

# check length of input paramenters
if len(sys.argv) < 2:
    print("No parameter passed to the script")
    exit(-1)


# py questionmanagement.py addq QUESTION CATEGORY IS_NEG
if sys.argv[1] == "addq":
    if len(sys.argv) == 5:
        try:
            category = models.Category.objects.get(name=sys.argv[3])
        except models.Category.DoesNotExist:
            print(f"Trying to insert a question in a not existing category.\n\
                Please, try to add the category using the following command;\n\
                    py questionmanagement.py addc \"{sys.argv[3]}\"")
            exit(-2)
        
        try:
            question = models.Question.objects.create(
                text=sys.argv[2],
                is_negative=sys.argv[4]
            )
        except IntegrityError:
            print("This question could already be in the database!")
            exit(-3)
        
        models.QuestionCategory.objects.create(
            question=question,
            category=category
        )
    else:
        print("The 'addq' command accept three parameters in the following order:\n\
            QUESTION - the text of the question, enclosed in quotes\n\
            CATEGORY - the category which the question belong to\n\
            IS_NEG - True if the question is phrased negatively, False otherwise")
        exit(0)

# py questionmanagement.py addc CATEGORY
elif sys.argv[1] == 'addc':
    if len(sys.argv) == 3:
        try:
            models.Category.objects.create(name=sys.argv[2])
        except IntegrityError:
            print("This category could already be in the database!")
            exit(-4)
    else:
        print("The 'addc' command accept one parameter:\n\
            CATEGORY - the category to be added")
        exit(0)

# py questionmanagement.py modifyq TEXTBEFORE TEXTAFTER
elif sys.argv[1] == 'modifyq':
    if len(sys.argv) == 4:
        try:
            question = models.Question.objects.get(text=sys.argv[2])
        except models.Question.DoesNotExist:
            print("This question does not exists within the database!")
            exit(-5)
        
        question.text = sys.argv[3]
        question.save()
    else:
        print("The 'modifyq' command accept two parameters in the following order:\n\
            TEXTBEFORE - the text of the question, enclosed in quotes, to be modified\n\
            TEXTAFTER - the new text of the question, enclosed in quotes")
        exit(0)

# py questionmanagement.py deleteq QUESTION
elif sys.argv[1] == 'deleteq':
    if len(sys.argv) == 3:
        try:
            question = models.Question.objects.get(text=sys.argv[2])
        except models.Question.DoesNotExist:
            print("This question is already not within the database!")
            exit(0)
        question.delete()
    else:
        print("The 'deleteq' command accept one parameter:\n\
            QUESTION - the text of the question, enclosed in quotes, to delete")
        exit(0)
