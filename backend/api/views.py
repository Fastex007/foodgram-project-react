import io

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.filters import AuthorTagFilter, IngredientSearchFilter
from api.models import (
    Favorite,
    Ingredient,
    NecessaryIngredient,
    Recipe,
    ShoppingCart,
    Tag
)
from api.pagination import PaginationLimit
from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    ShortRecipeSerializer,
    TagSerializer
)
from constants.types import MessageTexts, MessageTypes
from users.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class TagsViewSet(ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (IsAdminOrReadOnly,)


class IngredientsViewSet(ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = PaginationLimit
    filter_class = AuthorTagFilter
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.create_object(Favorite, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_object(Favorite, request.user, pk)
        return None

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.create_object(ShoppingCart, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_object(ShoppingCart, request.user, pk)
        return None

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = NecessaryIngredient.objects.annotate(
            total_amount=Sum('amount')
        ).values(
            'total_amount',
            'ingredient__name',
            'ingredient__measurement_unit'
        ).filter(
            recipe__shoppingcart__user=request.user
        )
        if ingredients:
            with io.StringIO() as recepies_ingredients:
                recepies_ingredients.write('Ингредиенты\n')
                for idx, data in enumerate(ingredients):
                    recepies_ingredients.write(
                        f'{idx + 1}.  {data.get("ingredient__name")} - '
                        f'{data.get("total_amount")} '
                        f'({data.get("ingredient__measurement_unit")})\n'
                    )
                recepies_ingredients.seek(0)
                response = HttpResponse(
                    recepies_ingredients.read().encode('utf-8'),
                    content_type='text/plain; charset=utf-8'
                )
                response['Content-Disposition'] = (
                    'attachment; filename="Список покупок.txt"'
                )
                return response

    def create_object(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({
                MessageTypes.Error:
                    MessageTexts.recepie_allready_contains_in_list
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_object(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            MessageTypes.Error: MessageTexts.recepie_allready_removed
        }, status=status.HTTP_400_BAD_REQUEST)
