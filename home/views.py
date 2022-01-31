from django.shortcuts import render

# Create your views here.
# Method to display the application home page
def display_home_page(request):
    # Gather recommendations
    return render(request, 'index.html')