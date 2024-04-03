from django.http import HttpResponse
from django.shortcuts import render, redirect
import re
from .models import Email
from .serializers import EmailSerializer
from rest_framework import generics


class EmailViewSet(generics.ListCreateAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer


class EmailDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer


def home(request):
    return render(request, 'home.html')


def analyze(request):
    if request.method == 'POST':
        # ['yalmaz ali<yalmaz.alizafar@gmail.com>']
        invalid_emails, names, emails = [], [], []

        # get text from form and split by either comma or semicolon
        entered_text = re.split(r"[,|;]", request.POST.get(
            'text', 'All are valid emails'))
        print(entered_text)
        if not entered_text == ['']:
            # split names and emails
            for index, user in enumerate(entered_text):
                if not '<' in user and not '>' in user:
                    continue
                names.append(user.split('<')[0])
                emails.append(user.split('<')[1].split('>')[0])
            print(names)

            # split the names in first and last name, the name can be 4 words long
            for index, name in enumerate(names):
                print(name)
                if name != '':
                    if len(name.split()) > 1 and len(name.split()) < 5:
                        names[index] = name.split()[0] + " " + name.split()[1]
                    else:
                        names[index] = name.split()[0]
                else:
                    names[index] = None
            print(names)
            print(emails)

            # check valid emails
            for index, email in enumerate(emails):
                if not re.fullmatch(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email):
                    invalid_emails.append(email)
                    print(email)
                    print(index)
                    emails.pop(index)
                    names.pop(index)

                    # invalid_emails.append(email)
                    # print(emails.index(email))
                    # emails.pop(emails.index(email))

            print(invalid_emails)
            print(names)

            # prepare params

            # create and save Email model instances
            for name, email in zip(names, emails):
                if name is None:
                    first_name, last_name = None, None
                else:
                    first_name, last_name = (name.split() + [None, None])[:2]
                Email.objects.create(firstName=first_name,
                                     lastName=last_name, email=email)
                print(first_name, last_name, email)

            params = {"invalidEmailsList": invalid_emails}
        else:
            params = {'invalidEmailsList': ['No email entered']}
        return render(request, 'analyze.html', params)
    else:
        return redirect('/')
