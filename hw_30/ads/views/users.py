from rest_framework.generics import *

from ads.serializers import *



class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer
