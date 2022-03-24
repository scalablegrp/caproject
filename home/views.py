from django.shortcuts import render
from .sqs_utils import SqsQueue

# Create your views here.
# Method to display the application home page
def display_home_page(request):
    #SqsQueue.create_and_consume_queue(request, "display_home_page")
    return render(request, 'index.html')

# Method to display error page
def display_error_page(request):
    return render(request, 'error.html')