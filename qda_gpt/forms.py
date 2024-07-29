# forms.py
from django import forms


class SetupForm(forms.Form):
    file = forms.FileField(label='Upload file')
    model_choice = forms.ChoiceField(
        choices=[
            ('gpt-3.5-turbo', 'GPT-3.5 Turbo'),
            ('gpt-4-turbo', 'GPT-4 Turbo'),
            ('gpt-4-turbo-preview', 'GPT-4 Turbo Preview'),
            ('gpt-4o-mini', 'GPT-4o mini'),
            ('gpt-4o', 'GPT-4o'),
            # Add other models here
        ],
        label='OpenAI model',
        initial='gpt-4o-mini'  # Set the default value here
    )

class AnalyzeForm(forms.Form):
    user_prompt = forms.CharField(label="Enter your prompt", max_length=1000)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

