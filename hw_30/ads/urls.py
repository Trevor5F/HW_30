from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ads.views import ads as ads_view, category as cat_view, users as users_view, selections as selections_view

urlpatterns = [
    path('cat/', cat_view.CategoryListView.as_view()),
    path('cat/<int:pk>/', cat_view.CategoryDetailView.as_view()),
    path('cat/create/', cat_view.CategoryCreateView.as_view()),
    path('cat/<int:pk>/update/', cat_view.CategoryUpdateView.as_view()),
    path('cat/<int:pk>/delete/', cat_view.CategoryDeleteView.as_view()),

    path('ad/', ads_view.AdListView.as_view()),
    path('ad/<int:pk>/', ads_view.AdDetailView.as_view()),
    path('ad/create/', ads_view.AdCreateView.as_view()),
    path('ad/<int:pk>/update/', ads_view.AdUpdateView.as_view()),
    path('ad/<int:pk>/delete/', ads_view.AdDeleteView.as_view()),
    path('ad/<int:pk>/upload_image/', ads_view.AdUploadImageView.as_view()),

    path('user/', users_view.UserListView.as_view()),
    path('user/<int:pk>/', users_view.UserDetailView.as_view()),
    path('user/create/', users_view.UserCreateView.as_view()),
    path('user/<int:pk>/update/', users_view.UserUpdateView.as_view()),
    path('user/<int:pk>/delete/', users_view.UserDeleteView.as_view()),

    path('user/token/', TokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),

    path('selection/', selections_view.SelectionListView.as_view()),
    path('selection/<int:pk>/', selections_view.SelectionDetailView.as_view()),
    path('selection/create/', selections_view.SelectionCreateView.as_view()),
    path('selection/<int:pk>/update/', selections_view.SelectionUpdateView.as_view()),
    path('selection/<int:pk>/delete/', selections_view.SelectionDeleteView.as_view()),
]