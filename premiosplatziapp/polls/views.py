from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Choice, Question
from django.views import generic


''' def index(request):
    latest_question_list = Question.objects.all()
    return render(request, "polls/index.html", {
        "latest_question_list" : latest_question_list
    })
    # return HttpResponse("Estas en la págima principal de premios platzi")

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id) # pk es predeterminado de Django (reservado para primary key)
    print(question.choice_set.all()) # de esta forma se busca todas las respuestas que pertenecen a la pregunta. choice es la tabla y _set metodo de python para buscar por llave primaria .all todas las r/ pertenecientes a la pregunta
    
    return render(request, "polls/detail.html",{
        "question":question
    })
    #question = Question.objects.get(pk=question_id)
    # return HttpResponse(f"estas viendo la pregunta numero {question_id}")

def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html",{
        "question" : question
    })
    #return HttpResponse(f"estas viendo los resultados de la pregunta numero {question_id}")
 '''

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        """return the last five published question """
        return Question.objects.order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

 
 
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError,Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "No elegiste una respuesta"
        } )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:result",args=(question.id,)))
                
    
    
    #return HttpResponse(f"estas votando a la pregunta numero {question_id}")
