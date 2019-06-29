from django import forms  
from .models import PostAd, DooSomething

SEASONS = (  
    ('2010', '2010'),
    ('2011', '2011'),
    ('2012', '2012'),
    ('2013', '2013'),
    ('2014', '2014'),
    ('2015', '2015'),
    ('2016', '2016'),
    ('2017', '2017'),
)

class SeasonForm(forms.ModelForm):  
    error_css_class = 'error'

    season = forms.ChoiceField(choices=SEASONS, required=True )

    class Meta:
        model = GameLog