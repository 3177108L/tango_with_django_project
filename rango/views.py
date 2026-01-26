from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings


def index(request):
    #Contsruct a dictionary to pass to the template engine as its context
    # Note the key boldmessage matches to {{ bold message }} in the template!
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}


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