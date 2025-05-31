from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.views import generic

# imported the bellow block for js post call implementation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


from .models import Question, Choice, TreatmentCenter, UserResponse
from django.shortcuts import redirect

#test using base index view



# this is the Center filter class with the custom functions if needed 
# class CenterFilter():
#     def __init__(self):
#             self.name = None
#             self.languages = None
#             self.lgbtq = True #FIX Test
#             self.insurrances = []
#             self.ss_payments = None
#             self.treat_model = []
#             self.
# fix me use json
testFilters = {
    "name" : None,
    "languages" : None, # array
    "lgbtq" : False,
    "insurances" : None, # array
    "ss_payments" : None,
    "spiritual" : None,
    "inpatient"  : None,
    "outpatient" : None,
    "med_assist"  : None, #bool
    "residential"  : None ,#bool
    "virtual"  : None, #bool
    "methedone" : None, #bool
    "suboxone" : None,#bool
    "transportation" : None, #bool
    "psych" : None
}

# def dict(self):
#     output = {}
#     for key, value in self.__dict__.items():
#         if value != None or value == []:
#             output[key] = value
#     return output
def dict(dict):
    output = {}
    for key, value in dict.items():
        if value != None or value == []:
            output[key] = value
       
    return output   


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


# set defualt filter as second argument
@csrf_exempt  # FIXMEif CSRF token is not being handled
def filteredlistView(request, filters = testFilters): #FIXMEuse generic list view maybe?
    centers = TreatmentCenter.objects.all()
    
    
    if not centers.exists():  # Check if no centers are available
        raise Http404("No treatment centers found")
    
    if request.method == "POST":
        # if request.POST.get('action') == "Start":
        #      return render(request, "projectApp/listView.html", {"centers": centers})
        #if request.POST.get('action') == "Submit":
        #used for ajax call
        try: 
            data = json.loads(request.body)
            test_filters = dict(filters)
            filterJson = json.dumps(test_filters)
            centers = centers.filter(**dict(data))
            #fixme use for AJAX if wanted
            #return JsonResponse( {'message': 'Success', 'filter': filterJson} )
            return render(request, "projectApp/cards.html", {"centers": centers, 'filter': dict(data)}) #version where filter does not

        except:
            data = None
            if filters != testFilters: 
                #FIXME when using config table convert to a loop instead
                filters['ss_payments'] = request.POST.get('check_ss_payments').checked
                filters['virtual'] = request.POST.get('check_virtual').checked
                filters['lgbtq'] = request.POST.get('check_LGBTQ').checked
            
            #holder = request.session.get('mydata')
            #if holder == None:    
            
            #request.session['mydata'] = test_filters
            
                #else:
                    # centers = centers.filter(**holder)
                    # request.session.pop('mydata')
            test_filters = dict(filters)
            centers = centers.filter(**test_filters)  # filtering can either be done with this way or with a specific loop "this is more adjustable"
            redirect("projectApp:list")
    if (filters != testFilters):
        return render(request, "projectApp/listView.html", {"centers": centers, 'filter': test_filters}) # Version when filter exsists
    else:
        return render(request, "projectApp/listView.html", {"centers": centers, 'filter': dict(filters)}) #version where filter does not
    # fixme use jsonresponse for ajax requests if wanted

currFilter = {
    "insurance" : [],
    "lgbtq" : True,
    "virtual" : True

}