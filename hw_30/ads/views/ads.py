import json


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad, Category, User
from ads.permissions import AdUpdateDeletePermission
from ads.serializers import AdSerializer, AdDestroySerializer


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def get(self, request, *args, **kwargs):
        categories = request.GET.getlist("cat", [])
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)

        text = request.GET.get("name")
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get("location")
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get("price_from")
        price_to = request.GET.get("price_to")
        if price_from:
            self.queryset = self.queryset.filter(price__gte=int(price_from))
        if price_to:
            self.queryset = self.queryset.filter(price__lte=int(price_to))

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author_id': ad.author_id,
            'author': ad.author.username,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'category_id': ad.category_id,
            'image': ad.image.url if ad.image else None},
            safe=False,
            json_dumps_params={'ensure_ascii': False})



@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = ('name', 'author', 'price', 'description', 'is_published', 'category')

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        new_ad = Ad.objects.create(
            name=ad_data['name'],
            author=get_object_or_404(User, pk=ad_data["author_id"]),
            price=ad_data['price'],
            description=ad_data['description'],
            is_published=ad_data['is_published'],
            category=get_object_or_404(Category, pk=ad_data["category_id"]),
        )

        return JsonResponse({
            'id': new_ad.id,
            'name': new_ad.name,
            'author_id': new_ad.author_id,
            'author': new_ad.author.username,
            'price': new_ad.price,
            'description': new_ad.description,
            'is_published': new_ad.is_published,
            'category_id': new_ad.category_id,
            'image': new_ad.image.url if new_ad.image else None},
            safe=False)



class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated, AdUpdateDeletePermission]
    serializer_class = AdSerializer



class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDestroySerializer
    permission_classes = [IsAuthenticated, AdUpdateDeletePermission]



@method_decorator(csrf_exempt, name="dispatch")
class AdUploadImageView(UpdateView):
    model = Ad
    fields = ('image',)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get('image', None)
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author_id,
            'author': self.object.author.username,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'category_id': self.object.category_id,
            'image': self.object.image.url if self.object.image else None},
            safe=False)



