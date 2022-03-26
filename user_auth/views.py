from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.shortcuts import render, redirect, reverse




# Login Functionality (NOT REQUIRED AS AWS COGNITO RESPONSIBLE FOR LOGIN) 
# def login(request):
#     # if the user is currently logged in direct them to the home page
#     if request.user.is_authenticated:
#         messages.info(request, "You are currently logged in")
#         return redirect(reverse('home'))
#     else:
#         # If the form has just been submitted
#         if request.method == "POST":
#             try:
#                 #if form.is_valid:
#                 user = auth.authenticate(email=request.POST['email'], password=request.POST['password'])
#                 # check if a user exists in the database matching the email address and password provided
#                 if user:
#                     auth.login(user=user, request=request)
#                     # If the login page was displayed by user trying to access particular page, redirect user to the page they were trying to access
#                     if 'next' in request.GET:
#                         return redirect(request.GET['next'])
#                     messages.info(request, "You are now logged in!")
#                     return redirect(reverse('home'))
#                 else:
#                     messages.info(request, "Login failed")
#                     return redirect(reverse('index'))
#             except Exception as e:
#                 print(e)
#                 messages.info(request, "An error occurred logging in")
#                 return redirect(reverse('login_form'))
#         # If the user isn't logged in, display the login page
#         try:
#             form = LoginForm()
#             return render(request, 'login.html', {'form': form})
#         except:
#             messages.info(request, "Error encountered loading the login page")
#             return redirect(reverse('home'))

    
    
# Function to display the registration form  (NOT REQUIRED AS AWS COGNITO RESPONSIBLE FOR REGISTRATION)  
# def register(request):
#     # Make sure the user is not currently logged in
#     if not request.user.is_authenticated:
#         # if the request is a post mapping, retrieve the submited forms details
#         if request.method == "POST":
#             # Try to create a customer usign the form's submitted values
#             try:
#                 # Make sure there isn't already a customer linked to that email address
#                 if CustomUser.objects.filter(email__iexact = request.POST.get('email')).exists():
#                     messages.info(request, "An issue occured registering this account holder details")
#                     return render(request, 'register.html')
#                 # If the email address is unique, register that user
#                 get_user_model().objects.create_customer(request.POST.get('f_name'), request.POST.get('l_name'), request.POST.get('email'), request.POST.get('password'))
#                 # Log the user in and redirect ot the home screen
#                 auth.authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
#                 messages.success(request, "You have successfully registered and can now log in")
#                 return redirect(reverse('login_form'))
#             except:
#                 messages.info(request, "There was an issue creating this account")
#                 return render(request, 'register.html')
#         else:
#             # If the request is a get mapping display, the registration form
#             return render(request, 'register.html')
#     else :
#         # If the user is already logged in, redirect them to the home page
#         messages.info(request, "Logged in users cannot access the Registration Form")
#         return redirect(reverse('home'))
    
# Function that allows user to log out
def logout(request):
    # Logout functionality needs to remove the 'cognito_details' key/value pairs from the session
    del request.session['cognito_details']
    messages.info(request, "Logout Successful")
    return redirect(reverse('home'))