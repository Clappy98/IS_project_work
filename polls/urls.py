from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('prepare/', views.prepareUser, name='prepareUser'),
    path('<str:userMappedStr>/', include([
        path('background/', include([
            path('select/', views.selectBackground, name='selectBackground'),
            path('register/', views.manageBackgroundSelection, name='manageBackgroundSelection'),
        ])),
        path('questionnaire/', include([
            path('prepare/', views.prepareQuestionnaire, name='prepareQuestionnaire'),
            path('<str:performanceName>/', include([
                path('show/', views.showQuestionnaire, name='showQuestionnaire'),
                path('register/', views.manageQuestionnaireAnswer, name='manageQuestionnaireAnswer')
            ]))
        ]))
    ]))
]