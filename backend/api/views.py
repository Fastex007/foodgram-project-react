import io

from api.filters import AuthorTagFilter, IngredientSearchFilter
from api.models import (Favorite, Ingredient, NecessaryIngredient, Recipe,
                        ShoppingCart, Tag)
from api.pagination import PaginationLimit
from api.serializers import (IngredientSerializer, RecipeReadSerializer,
                             RecipeWriteSerializer, ShortRecipeSerializer,
                             TagSerializer)
from constants.types import MessageTexts, MessageTypes
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from users.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class TagsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PaginationLimit
    filter_class = AuthorTagFilter
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    serializer = get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'GET':
            return self.add_obj(Favorite, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(Favorite, request.user, pk)
        return None

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'GET':
            return self.add_obj(ShoppingCart, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(ShoppingCart, request.user, pk)
        return None

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = NecessaryIngredient.objects.filter(
            recipe__shoppingcart__user=request.user
        ).annotate(total_amount=Sum('ingredient__amount'))

        if ingredients:
            with io.StringIO() as recepies_ingredients:
                recepies_ingredients.write('Ингредиенты\n')
                for idx, data in enumerate(ingredients):
                    recepies_ingredients.write(
                        f'{idx}.  {data.get("name")} - '
                        f'{data.get("total_amount")} '
                        f'({data.get("measurement_unit")})\n'
                    )
                recepies_ingredients.seek(0)
                return HttpResponse(
                    recepies_ingredients.read().encode('cp1251'),
                    headers={
                        'Content-Type': 'text/plain; charset=cp1251',
                        'Content-Disposition':
                            'attachment;'
                            'filename="Список покупок.txt"'
                    },
                )

    def add_obj(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({
                MessageTypes.Error:
                    MessageTexts.recepie_allready_contains_in_list
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            MessageTypes.Error: MessageTexts.recepie_allready_removed
        }, status=status.HTTP_404_NOT_FOUND)
