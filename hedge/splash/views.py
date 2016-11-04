from django.shortcuts import render

def base_view(request):
	return render(request, 'splash/main.html', {})

def glossary_view(request):
	return render(request, 'splash/glossary.html', {})
