from django.db import models


class Email(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50, null=True, blank=True)
    lastName = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254)

    def __str__(self):
        if self.firstName and self.lastName:
            return self.firstName + " " + self.lastName + " <" + self.email + ">"
        elif self.firstName and not self.lastName:
            return self.firstName + " <" + self.email + ">"
        elif self.lastName and not self.firstName:
            return "NONE" + "" + self.lastName + " <" + self.email + ">"
        else:
            return "<" + self.email + ">"
# Path: analyze/serializers.py
