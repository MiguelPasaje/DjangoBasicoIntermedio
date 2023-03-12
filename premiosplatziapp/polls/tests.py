import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question

# Create your tests here.
# se van a testear 
# modelos o vistas

class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_questions(self):
        """debe retornar falso si se pone una pregunta con fecha del futuro"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text = '¿Quién es el mejor Course Director de platzi', pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)
        
    def test_was_published_recently_with_present_questions(self):
        """debe retornar true si se pone una pregunta con fecha de hoy"""
        time = timezone.now()
        future_question = Question(question_text = '¿Quién es el mejor Course Director de platzi', pub_date=time)
        self.assertIs(future_question.was_published_recently(),True)
        
    def test_was_published_recently_with_past_questions(self):
        """debe retornar falso si se pone una pregunta con fecha del pasado"""
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(question_text = '¿Quién es el mejor Course Director de platzi', pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)
 
def create_question(question_text,days):
    """
        Create a question with the given,"question_text" and published the given
        number of daus offset to now (negative for questions published in the past,
        positive for questions that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
       
class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """ si no existe nunguna pregunta en BD vamos a poner un mensaje apropiado """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])
  
    def test_future_question(self):
        """
            Question with a pub_date in the future aren't displayed on the index page.
        """     
        create_question("future question",days = 30)   
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response,"No polls are available.") 
        self.assertQuerysetEqual(response.context["latest_question_list"],[])
        
        
    def test_past_question(self):
        """
            Questions with a pub_date in the past are displayed on the index page
        """
        question = create_question("pst question",days = -10)   
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])

    def test_future_question_and_past_question(self):
        """
            even if both past and future question exist, only past questions are displayed
        """
        past_question = create_question(question_text="past question", days=-30)
        future_question = create_question(question_text="future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )
        
    
    def test_two_past_question(self):    
        """
            the questions index page may display multiple question
        """
        past_question1 = create_question(question_text="past 1 question", days=-30)
        past_question2 = create_question(question_text="past 2 question", days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1,past_question2]
        ) 
    def test_two_future_question(self):    
        """
            the question index page should not show questions from the future
        """
        past_question1 = create_question(question_text="past 1 question", days=30)
        past_question2 = create_question(question_text="past 2 question", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        ) 
    
class QuestionDeatilViewTest(TestCase):
    
    def test_future_Question(self):
        """
            the detail view of a question quth a pub_date in the future
            returns a 404 error not dount
        """
        future_question = create_question(question_text="future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,)) #puede ir future_question.pk _-> es lo mismo
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        

    def test_past_Question(self):
        """
            the detail view of a question with a pub_date in the past display 
            the question's text            
        """
        past_question = create_question(question_text="past question", days=-30)
        url = reverse("polls:detail", args=(past_question.id,)) #puede ir future_question.pk _-> es lo mismo
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
#crear los test para results-view