from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from constants.types import MessageTexts

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=10,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    RED = 'FF0000'
    GREEN = '#008000'
    BLUE = '#0000FF'

    TAG_COLORS = [
        (RED, 'Красный'),
        (GREEN, 'Зеленый'),
        (BLUE, 'Синий'),
    ]

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        choices=TAG_COLORS,
        verbose_name='HEX цвет'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name}_{self.color}_{self.slug}'


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название')
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение'
    )
    text = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='NecessaryIngredient',
        verbose_name='Ингредиент',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                1,
                message=MessageTexts.min_cooking_time
            ),
        ),
        verbose_name='Время приготовления, мин'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.name}_{self.author}'


class NecessaryIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                1, message=MessageTexts.min_ingredients_count
            ),
        ),
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Необходимый ингредиент'
        verbose_name_plural = 'Необходимые ингредиенты'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique ingredients recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe}_{self.ingredient}_{self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique favorite recipe for user'
            )
        ]

    def __str__(self):
        return f'{self.user}_{self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique shoppingcart user'
            )
        ]

    def __str__(self):
        return f'{self.user}_{self.recipe}'
