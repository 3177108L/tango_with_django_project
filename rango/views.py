from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rango.models import Category
from rango.models import Page

from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse

from rango.forms import UserForm, UserProfileForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect




def index(request):
    # query database for a list of all categories currently stored
    # order the categories by the number of likes in descending order
    # retireve the top 5 only --or less than 5.
    # place the list in our context_dixt dictionary
    # that will be passed to the template enging
    category_list = Category.objects.order_by('-likes')[:5]


    #Contsruct a dictionary to pass to the template engine as its context
    # Note the key boldmessage matches to {{ bold message }} in the template!
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list


    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list


    return render(request, 'rango/index.html', context=context_dict)

    # return HttpResponse("Rango says hey there partner!<br />"
    #     "<a href='/rango/about/'>About</a>")


def about(request):
     #Contsruct a dictionary to pass to the template engine as its context
    # Note the key boldmessage matches to {{ bold message }} in the template!
    context_dict = {'name': 'Frida', 'MEDIA_URL': settings.MEDIA_URL}

    
    return render(request, 'rango/about.html', context=context_dict)
    # return HttpResponse( "Rango says here is the about page. <br />"
    #     "<a href='/rango/'>Index</a>" )


def show_category(request, category_name_slug):
    # create context dictionary which we can pass to template rendering engine
    context_dict = {}

    try:
        # Is there a category name slug with the given name?
        # if we can't the get() method raises a DonesntExist exeception
        #  get() method returns one model instance or raises an exception
        category = Category.objects.get(slug=category_name_slug)

        # Retirve all of the associated pages
        # filter() will return a lost of page objects or an empty list
        pages = Page.objects.filter(category = category)
    # adds results list to template context under name pages
        context_dict['pages'] = pages
        # all add the category object from te database to contect dictionary
        # we use this in template to verify that the category exists
        context_dict['category'] = category
        context_dict['category_name'] = category.name

    except:
        # if we din't find specified category, don't do anything
        # template will display the 'no category' message for us
        context_dict['category'] = None
        context_dict['category_name'] = None
        context_dict['pages'] = None


# render response and return to client  
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided a valid form?
        if form.is_valid():
            # save the new category to the database
            form.save(commit=True)

        #  category is saved, we need to confirm
        # redirect user back to index view
            return redirect('/rango/')
        
        # supplidec form contained errors
        # print to terminal
        else:
            print(form.errors)

    # will handle the bad form, new form or no form supplied cases
    # render form with error messages
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')
    
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
    
    if form.is_valid():
    
        if category:
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
    # value for telling templayte if registration was successful 
    # Set to False intially, code changed to True if registration succeeds

    registered = False

    # HTTP POST, process the the form data 
    if request.method == 'POST':
        # grab information from raw form info
        # using both UserForm and UserProfileForm
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # save user to database
            user = user_form.save()

            # has the poassword and update user object
            user.set_password(user.password)
            user.save()

            # UserProfile instance
            profile = profile_form.save(commit=False)
            profile.user = user

            # did the user provide a profile picture
            # get from input form and att to UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # save the UserProfile instance
            profile.save()

            # update variable to indicate template reg was successful
            registered = True

        else:
            # invalid form or forms
            # print problems to terminal
            print(user_form.errors, profile_form.errors)
    else:

        # not http post, render form using ModelForm instances
        # blank forms for user input
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', context = {'user_form': user_form, 'profile_form': profile_form,'registered': registered})


def user_login(request):
    # if request is HTTP post, pull out relevent info
    # Gather username and password provided by the user.
    # This information is obtained from the login form.
    # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'], because the
    # request.POST.get('<variable>') returns None if the value does not exist, while request.POST['<variable>']
    #  will raise a KeyError exception.

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
        # Is the account active? It could have been disabled.
            
            if user.is_active:
            # If the account is valid and active, we can log the user in.
            # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
            # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
            # The request is not a HTTP POST, so display the login form.
            # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html')
    
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))