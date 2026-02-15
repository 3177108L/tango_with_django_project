import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    # create lists of dictionaries containg pages we want to add ino each category
    # then create a dictionary of dictionaryes for our categperies
    # allows ut to iterate through each data structure, and add data to our models
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url':'http://docs.python.org/3/tutorial/',
         'views': 100
         },
         {'title':'How to Think like a Computer Scientist',
          'url':'http://www.greenteapress.com/thinkpython/',
          'views': 200},
          {'title':'Learn Python in 10 Minutes',
           'url':'http://www.korokithakis.net/tutorials/python/',
           'views': 100} ]
    
    django_pages = [{'title':'Official Django Tutorial',
                     'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
                     'views': 10},
                    {'title':'Django Rocks',
                     'url':'http://www.djangorocks.com/',
                     'views': 20},
                     {'title':'How to Tango with Django',
                      'url':'http://www.tangowithdjango.com/',
                      'views': 50} ]
    
    other_pages = [
        {'title':'Bottle',
         'url':'http://bottlepy.org/docs/dev/',
         'views': 70},
         {'title':'Flask',
          'url':'http://flask.pocoo.org',
          'views': 190} ]
    

    cats = {'Python': {'pages': python_pages,
                       'views': 128,
                       'likes': 64},
            'Django': {'pages': django_pages,
                       'views': 64,
                       'likes': 32},
            'Other Frameworks': {'pages': other_pages,
                                   'views': 32,
                                   'likes': 16} 
                                   
            }
    


    # this goes through the cats dictionary, adds each category
    # and adds all the associated pages for that category
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])

    # print out the categroeis we have added
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')


# two functions
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views= views
    p.save()
    return p

def add_cat(name, views = 0, likes = 0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c



# start execution here
# allows python module to act as wither a reusable module or a standalone Python script
# reusable module, one that can be imported into other modules
# standalone would be executed from terimanl by entering python module.pu
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()


