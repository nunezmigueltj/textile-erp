from django.shortcuts import render

# Create your views here.
def garments_list(request):
    return render(request, 'garments/garments_list.html', {})