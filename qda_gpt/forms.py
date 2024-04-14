# forms.py
from django import forms


class SetupForm(forms.Form):
    file = forms.FileField(label='Upload file')
    model_choice = forms.ChoiceField(choices=[
        ('gpt-3.5-turbo', 'GPT-3.5 Turbo'),
        ('gpt-3.5-turbo-0125', 'GPT-3.5 Turbo 16K (0125)'),
        ('gpt-4', 'GPT-4'),
        ('gpt-4-32k', 'GPT-4 32K'),
        ('gpt-4-turbo', 'GPT-4 Turbo'),
        ('gpt-4-preview', 'GPT-4 Turbo Preview'),
        # Add other models here
    ], label='OpenAI model')

class AnalyzeForm(forms.Form):
    user_prompt = forms.CharField(label="Enter your prompt", max_length=1000)


