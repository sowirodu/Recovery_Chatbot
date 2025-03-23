from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.views import generic

from .models import Question, Choice, TreatmentCenter, UserResponse
from django.shortcuts import redirect

#test using base index view
class IndexView(generic.ListView):
    template_name = "projectApp/listView.html"
    context_object_name = "centers"

    def get_queryset(self):
        """Return the last five published questions."""
        return TreatmentCenter.objects.order_by("name")[:5]
    
    



def index(request):
    # Redirect to the first question (if available)
    first_question = Question.objects.order_by("pub_date").first()
    if first_question:
        return redirect("projectApp:details", question_id=first_question.id)
    else:
        return HttpResponse("No questions are available.")


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)



def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()

    # Handle form submission for user response
    if request.method == "POST":
        choice_id = request.POST.get("choice")
        if choice_id:
            choice = get_object_or_404(Choice, pk=choice_id)
            UserResponse.objects.create(question=question, choice=choice)

            # Redirect to the next question (if available)
            next_question = Question.objects.filter(pub_date__gt=question.pub_date).first()
            if next_question:
                return redirect("projectApp:details", question_id=next_question.id)
            else:
                return HttpResponse("Thank you for completing the questions!")

    return render(request, "projectApp/detail.html", {"question": question, "choices": choices})

#create list view
def listView(request):
    centers = TreatmentCenter.objects.all()
    
    if not centers.exists():  # Check if no centers are available
        raise Http404("No treatment centers found")
    
    
    return render(request, "projectApp/listView.html", {"centers": centers})



def filteredlistView(request):
    centers = TreatmentCenter.objects.all()
    
    if not centers.exists():  # Check if no centers are available
        raise Http404("No treatment centers found")
    
    if request.method == "POST":
        if request.POST.get('action') == "Submit":
           lgbtq = request.POST.get('check_LGBTQ')
           if(lgbtq):
               centers = centers.filter(lgbtq=lgbtq)

    return render(request, "projectApp/listView.html", {"centers": centers})

    

currFilter = {
    "insurance" : [],
    "lgbtq" : True,
    "virtual" : True

}