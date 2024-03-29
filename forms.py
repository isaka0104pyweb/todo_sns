from django import forms
from.models import Message,Good
from django.contrib.auth.models import User

from .models import Todo

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            "content":forms.Textarea(attrs={"class":"form-control","rows":2})
        }

class PostForm(forms.Form):
  content = forms.CharField(max_length=500, \
    widget=forms.Textarea(attrs={'class':'form-control', 'rows':2}))
    
  def __init__(self, user, *args, **kwargs):
    super(PostForm, self).__init__(*args, **kwargs)




class TodoForm(forms.ModelForm):
    gen=forms.ChoiceField(
        choices=[
                ("20代","20代"),
                ("30代","30代"),
                ("40代","40代"),
                ("50代","50代"),
            ])
    class Meta:
        model = Todo
        fields = ['title', 'description','deadline',"gen"]
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),}

