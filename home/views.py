from django.shortcuts import render

# Create your views here.
# Method to display the application home page
def display_home_page(request):
    try:
        return render(request, 'index.html')
    except Exception as e:
        print(e)

# Method to display error page
def display_error_page(request):
    return render(request, 'error.html')