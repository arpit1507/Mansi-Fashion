import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','myproject.settings')

import django
django.setup()

import random
from first_app.models import AccessRecord,Topic,Webpage,Users
from faker import Faker

fakgen=Faker()
topics=['Search','Social','Marketplace','News','Games']

def add_topic():
    t= Topic.objects.get_or_create(top_name=random.choice(topics))[0]
    t.save()
    return t

def populate(N=5):
    for entry in range(N):
        #top=add_topic()
        #fake_url=fakgen.url()
        #fake_date=fakgen.date()
        fake_name=fakgen.company()
        name=fakgen.name()
        first_name,last_name=name.split(" ")[0],name.split(" ")[1]
        email=first_name+'.'+last_name+"@"+fake_name+".com"
        #webpg=Webpage.objects.get_or_create(topic=top,url=fake_url,name=fake_name)[0]
        user=Users.objects.get_or_create(First_name=first_name,Last_name=last_name,Email=email)[0]
        #acc_rec=AccessRecord.objects.get_or_create(name=webpg,date=fake_date)[0]

if __name__=='__main__':
    print("populating the script")
    populate(20)
    print("population Complete")

