from rest_framework import serializers

from ads.models import Location, User, Ad, Category, Selection


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'role']

class UserDetailSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field="name"
    )
    class Meta:
        model = User
        exclude = ['password']

class UserCreateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = User
        fields = '__all__'



    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(user.password)
        user.save()

        for location in self._locations:
            obj, _ = Location.objects.get_or_create(name=location)
            user.location.add(obj)
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        queryset=Location.objects.all(),
        many=True,
        slug_field="name"
    )

    def is_valid(self, raise_exception=False):
        if 'locations' in self.initial_data:
            self._locations = self.initial_data.pop("locations")
        else:
            self._locations = []
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        for location in self._locations:
            obj, _ = Location.objects.get_or_create(name=location)
            user.location.add(obj)
        return user

    class Meta:
        model = User
        fields = '__all__'

class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]

#______________________________________________________________

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

#_______________________________________________________________

class AdSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        queryset=User.objects.all(),
        slug_field='username'
    )

    category = serializers.SlugRelatedField(
        required=False,
        queryset=Category.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Ad
        fields = '__all__'

class AdDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["id"]

#______________________________________________________________

class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        exclude = ["items"]


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'

class SelectionDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id"]