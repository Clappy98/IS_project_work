from django.shortcuts import render
from django.db.models import Model
from django.http import HttpResponse, HttpResponseRedirect
import random
import hashlib
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
    print(user_mapping_dict)

def get_user_from_string(str):
    global user_mapping_dict
    return user_mapping_dict[str]

def remove_user_mapping(str):
    global user_mapping_dict
    user_mapping_dict.pop(str, None)

# se si resetta il server, viene svuotato
# un utente potrebbe non essere in grado di
# completare il questionario se accadesse durante
# la compilazione
user_mapping_dict = {
}

# codifica sha dell'id dell'user
def get_sha():
    pass


# Create your views here.

def test(request):
    return render(
        request,
        'polls/test.html',
        context={
            'performance':Performance.objects.get_or_create(
                name='testPerformance',
                year=2022,
                duration=120,
                link="https://www.youtube.com/embed/O91DT1pR1ew"
            )[0],
            'musicGenre':'test1',
            "AITechnique":'test2',
            'categories':Category.objects.all().order_by('?'),
            'likertValues':range(1,6),
            'userMappedStr':'loljknoidea'
        }
    )

# gestisce la homepage del sito
def homepage(request):
    # conta se sono presenti delle performance
    count = Performance.objects.exclude(link__isnull=True).count()

    return render(
        request,
        'polls/homepage.html',
        context={
            'count':count,
        }
    )

# dopo aver cliccato su 'Avvia Questionario' viene generato
# un utente e la sua stringa identificativa
def prepareUser(request):
    #user = get_sha()
    user = User.objects.create()

    userMappedStr = get_random_string_from_user(user.pk)
    add_mapping(userMappedStr, user.pk)

    bgs = Background.objects.all()
    count = bgs.count()

    # non ci sono background da scegliere
    if(count==0):
        return HttpResponseRedirect(reverse('prepareQuestionnaire', args=[userMappedStr]))
    # esiste un solo background, viene fatta in automatico l'associazione
    elif(count==1):
        return HttpResponseRedirect(reverse('manageBackgroundSelection', args=[userMappedStr, bgs[0].type]))
    else:
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
def manageBackgroundSelection(request, userMappedStr, bg):
    background = Background.objects.get(pk=bg)
    userId = get_user_from_string(userMappedStr)
    user = User.objects.get(pk=userId)
    
    Experience.objects.create(background=background, user=user)
    
    return HttpResponseRedirect(reverse('prepareQuestionnaire', args=[userMappedStr]))

# dopo aver ultimato la creazione dell'utente, viene
# scelta una performance casuale da cui iniziare il questionario
# è assicurato che ci sia almeno una performance, altrimenti non
# si potrebbe arrivare a questo URL
def prepareQuestionnaire(request, userMappedStr):
    startingPerformance = Performance.objects.exclude(link__isnull=True).order_by('?').first().name

    return HttpResponseRedirect(reverse('showQuestionnaire', args=[userMappedStr, startingPerformance]))

# mostra la pagina del questionario
def showQuestionnaire(request, userMappedStr, performanceName):
    performance = Performance.objects.get(pk=performanceName)
    
    try:
        musicGenre = performance.performancecharacteristic_set.get(attribute='musicGenre').value
    except PerformanceCharacteristic.DoesNotExist:
        musicGenre = "Not defined"
    
    try:
        AITechnique = performance.performancecharacteristic_set.get(attribute='AItechnique').value
    except PerformanceCharacteristic.DoesNotExist:
        AITechnique = "Not defined"
    
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