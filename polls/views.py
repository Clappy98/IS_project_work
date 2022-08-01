from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import random
import string

from django.urls import reverse
from .models import *


def get_random_string_from_user(userId):
    global user_mapping_dict
    output_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(15))
    return output_string

def add_mapping(userStr, userId):
    global user_mapping_dict
    user_mapping_dict[userStr] = userId

def get_user_from_string(str):
    global user_mapping_dict
    return user_mapping_dict[str]

def remove_user_mapping(str):
    global user_mapping_dict
    user_mapping_dict.pop(str, None)


user_mapping_dict = {
    'test':0
}



# Create your views here.

# gestisce la homepage del sito
def homepage(request):
    return render(request, 'polls/homepage.html')

# dopo aver cliccato su 'Avvia Questionario' viene generato
# un utente e la sua stringa identificativa
def prepareUser(request):
    user = User.objects.create()

    userMappedStr = get_random_string_from_user(user.pk)
    add_mapping(userMappedStr, user.pk)

    return HttpResponseRedirect(reverse('selectBackground', args=[userMappedStr]))

# dopo la creazione dell'utente, verrà mostrata una pagina in cui 
# verrà chiesto di scegliere il proprio background
def selectBackground(request, userMappedStr):
    return render(
        request,
        'polls/selectBackground.html',
        context={
            'backgrounds':Background.objects.all(),
            'userMappedStr':userMappedStr
        }
    )

# inserisce la relazione tra user e background nel database
def manageBackgroundSelection(request, userMappedStr):
    if request.method == 'POST':
        ans = request.POST['background']

        background = Background.objects.get(pk=ans)
        userId = get_user_from_string(userMappedStr)
        user = User.objects.get(pk=userId)

        Experience.objects.create(
            user=user,
            background=background
        )

        return HttpResponseRedirect(reverse('prepareQuestionnaire', args=[userMappedStr]))

# dopo aver ultimato la creazione dell'utente, viene
# scelta una performance casuale da cui iniziare il questionario
def prepareQuestionnaire(request, userMappedStr):
    startingPerformance = Performance.objects.all().order_by('?').first().name

    return HttpResponseRedirect(reverse('showQuestionnaire', args=[userMappedStr, startingPerformance]))

# mostra la pagina del questionario
def showQuestionnaire(request, userMappedStr, performanceName):
    performance = Performance.objects.get(pk=performanceName)
    musicGenre = performance.performancecharacteristic_set.get(attribute='musicGenre').value
    AITechnique = performance.performancecharacteristic_set.get(attribute='AItechnique').value

    return render(
        request,
        'polls/showQuestionnaire.html',
        context={
            'performance':performance,
            'musicGenre':musicGenre,
            "AITechnique":AITechnique,
            'categories':Category.objects.all().order_by('?'),
            'likertValues':range(1,6),
            'userMappedStr':userMappedStr
        }
    )


def manageQuestionnaireAnswer(request, userMappedStr, performanceName):
    performance = Performance.objects.get(pk=performanceName)
    userId = get_user_from_string(userMappedStr)
    user = User.objects.get(pk=userId)

    if request.method == 'POST':
        # legge i dati inviati tramite POST
        for question in Question.objects.all():
            answer = request.POST.get(question.text)

            if answer != None:
                Answer.objects.create(
                    user=user,
                    performance=performance,
                    question=question,
                    value=answer
                )

        # qui si constrolla se l'utente ha finito di compilare il questionario
        performancesViewedByTheUser = user.answer_set.values_list('performance', flat=True).distinct()  # ritorna un elenco di PK, non oggetti

        # l'utente ha fornito una risposta per tutte le performance per cui è disponibile il video
        if performancesViewedByTheUser.count() == Performance.objects.exclude(link__isnull=True).count():
            remove_user_mapping(userMappedStr)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            # rimanda l'utente ad un nuovo questionario
            nextPerformance = Performance.objects.exclude(pk__in=performancesViewedByTheUser).order_by('?').first().name
            return HttpResponseRedirect(reverse('showQuestionnaire', args=[userMappedStr, nextPerformance]))