from api.views import IngredientsViewSet, RecipeViewSet, TagsViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('tags', TagsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
