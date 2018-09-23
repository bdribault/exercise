from datetime import date

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Complete the standard User information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()

    @property
    def age(self):
        """
        Age of the user, based on its birthday

        Beware, in contrary to birthday, the age will change according to the current date. Keep that
        in mind while testing.

        """
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    def __str__(self):
        return self.user.username
