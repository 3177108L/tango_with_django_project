from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rango.models import Category
from rango.models import Page

from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse

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