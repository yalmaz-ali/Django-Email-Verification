from django.http import HttpResponse
from django.shortcuts import render
import re


def home(request):
    return render(request, 'home.html')


def analyze(request):
    # ['yalmaz ali<yalmaz.alizafar@gmail.com>']
    invalid_emails, names, emails = [], [], []

    # get text from form and split by either comma or semicolon
    entered_text = re.split(r"[,|;]", request.GET.get(
        'text', 'All are valid emails.'))
    print(entered_text)

    # split names and emails
    for index, user in enumerate(entered_text):
        names.append(user.split('<')[0])
        emails.append(user.split('<')[1].split('>')[0])

    # split the names in first and last name, the name can be 4 words long
    for index, name in enumerate(names):
        if len(name.split()) > 1 and len(name.split()) < 5:
            names[index] = name.split()[0] + " " + name.split()[1]
        else:
            names[index] = name.split()[0]
    print(names)
    print(emails)

    # check valid emails
    for email in emails:
        if not re.fullmatch(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email):
            invalid_emails.append(email)
            emails.remove(email)

    print(invalid_emails)
    # prepare params
    params = {"invalidEmailsList": invalid_emails}
    return render(request, 'analyze.html', params)
