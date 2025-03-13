from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

from .models import Question, Choice, UserResponse
from django.shortcuts import redirect

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