import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext  as _



# Create your models here.

#CURRENTLY NOT USED
class Location(models.Model):
    Name = models.CharField(max_length=200)
    id = models.SmallIntegerField(primary_key=True)

# Question Model
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    
    def __str__(self):
        return self.question_text


# List of all choices for that question

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text

# Stores the question and the choice the user chose.

class UserResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.question}: {self.choice}"

#Model Denotes the Insurance and Insurance type used in a list of the treatment centeer and response for the questions

class Insurance(models.Model):
    name =models.CharField(max_length= 100, unique=True)
    type = models.CharField(max_length = 10, default="Standard") # not sure if this is really needed
    def __str__(self):
            return self.name
    

#Model Denotes the treatment style plan used in a list of the treatment center and response for the questions

class Treatment_Model(models.Model):
    name= models.CharField( max_length= 100,unique=True)
    def __str__(self):
            return self.name



#This model is for The treatment center location and all of the associated data
#currently needs to store 51 locations and all associated data

class TreatmentCenter(models.Model):
    name = models.CharField(unique=True, max_length=200)
    address_1 = models.CharField(_("Address"), max_length=128, default= "Unknown")
    address_2 = models.CharField(_("Address cont'd"), max_length=128, blank=True,default= "Unknown")
    city = models.CharField(_("City"), max_length = 64, default = "San Antonio")
    State = models.CharField(max_length=2, default= "TX")
    zipcode = models.IntegerField() #might want to change to geo location for calculations

    SPANISH = "SPAN"
    ENGLISH = "ENG"
    ENGLISH_SPANISH = "ENSP"
    OTHER ="OTH"
    UNKNOWN = "UNKN"
    class Languages(models.TextChoices):
        SPANISH = "SPAN", "Spanish"
        ENGLISH = "ENG", "English"
        ENGLISH_SPANISH = "ENSP", "English/Spanish"
        OTHER = "OTH", "Other"
        UNKNOWN = "UNKN", "Unknown"
    languages = models.CharField(
        max_length=5,  # Adjust based on the longest choice value
        choices=Languages.choices,  # Reference `.choices` correctly
        default=Languages.ENGLISH  # Use class attribute for clarity
    )
    insurances= models.ManyToManyField(Insurance, verbose_name= "Valid Insurances") # might need new parameters
    
    ss_payments = models.BooleanField(default=False,verbose_name ="Sliding Scale Payment") # bool key Note potentially use NUll vaireable to denote if empty values are set as null and not false
    treat_model = models.ManyToManyField(Treatment_Model) # table of model strings use foreign key on another model
    spiritual = models.BooleanField(default=False)
    lgbtq = models.BooleanField(default=False)   # LGBTQ #bool
    inpatient  = models.BooleanField(default=False)#bool
    outpatient = models.BooleanField(default=False)#bool
    med_assist  = models.BooleanField(default=False)#bool
    residential  = models.BooleanField(default=False)#bool
    virtual  = models.BooleanField(default=False)#bool
    methedone  = models.BooleanField(default=False)#bool
    suboxone  = models.BooleanField(default=False)#bool
    transportation  = models.BooleanField(default=False)#bool
                # phone_num There are some phone number widgets and other handlers to potentiall use
    psych  = models.BooleanField(default=False)#bool
                # age #num or limited value denoting state
    hyperlink = models.URLField(default="https://www.youtube.com/")
    description = models.CharField(max_length= 500, default="Currently Blank: Will be updated") # can be expanded on
    # notes
    active_choices = (
         
         ('true','Active'),
         ('false','Inactive'),
         ('null', "Unkown")
    )
    active = models.CharField(max_length=10, choices=active_choices, default ="null")
    #For active null is not yet aproved, true is approved, and false is rejected/inactive  
    def __str__(self):
        return self.name
    

    #does there need to be a model for the questions/answers?
#    Extra:
    
    #is id needed
    #criminal record limitation
    #citizen ship





    #51 locations

# class Input(models.Model):
#     answers = models.ManyToManyField(Choice)