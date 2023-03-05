from django.contrib import admin
from .models import Question , Choice


#de esta manera observo en la pantalla de administacion la seccion de Polls y sus Question

admin.site.register(Question)

admin.site.register(Choice)
