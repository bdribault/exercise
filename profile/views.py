from django.contrib.auth.models import User
from rest_framework import generics

from profile.serializers import UserSerializer, DetailedUserSerializer


class DetailedUser(generics.RetrieveAPIView):
    """
    Get the detailed version of a user (+ profile) based on the primary key given in the url.
    """
    queryset = User.objects.all()
    serializer_class = DetailedUserSerializer


class UserList(generics.ListAPIView):
    """
    Get a user list according to optionals filters given as url parameters (no filter : all users)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()

        year = self.request.GET.get('year', None)
        max_age = self.request.GET.get('max_age', None)
        min_age = self.request.GET.get('min_age', None)
        age = self.request.GET.get('age', None)

        if year:
            # If year and filters are used, only year will be taken in account
            return queryset.filter(profile__birthday__year=year)

        if age:
            # If age and max_age/min_age are used, only age is used
            return [u for u in queryset if u.profile.age == int(age)]

        # max_age and min_age filters can be used together
        if max_age:
            queryset = [u for u in queryset if u.profile.age <= int(max_age)]

        if min_age:
            queryset = [u for u in queryset if u.profile.age >= int(min_age)]

        return queryset
