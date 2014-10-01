from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm


@login_required
def home(request):
	return render(request, 'base_layout.html')
