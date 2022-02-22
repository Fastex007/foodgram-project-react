class TypesBase:
    _titles = {}

    @classmethod
    def stringify(cls, ntype, default=None):
        return cls._titles.get(ntype, default)

    @classmethod
    def ui_data(cls):
        return [{'type': ntype, 'title': title}
                for ntype, title in cls._titles.items()]


class MessageTypes(TypesBase):
    Error = 1

    _titles = {
        Error: 'error',
    }


class MessageTexts(TypesBase):
    self_subscribing = 1
    allready_subscribed = 2
    self_unsubscribing = 3
    allready_unsubscribed = 4
    no_ingredients = 5
    not_unique_ingredients = 6
    no_ingredient_count = 7
    recepie_allready_contains_in_list = 8
    recepie_allready_removed = 9
    min_cooking_time = 10
    min_ingredients_count = 11

    _titles = {
        self_subscribing: 'Вы не можете подписываться на самого себя',
        allready_subscribed: 'Вы уже подписаны на данного пользователя',
        self_unsubscribing: 'Вы не можете отписываться от самого себя',
        allready_unsubscribed: 'Вы уже отписались от данного пользователя',
        no_ingredients: 'Не выбрано ни одного ингредиента',
        not_unique_ingredients: 'Данный ингредиент уже выбран',
        no_ingredient_count: 'Не указано количество',
        recepie_allready_contains_in_list: 'Рецепт уже добавлен в список',
        recepie_allready_removed: 'Рецепт уже удален',
        min_cooking_time: 'Время приготовления должно быть >= 1 минут',
        min_ingredients_count: 'Минимальное ингредиентов должно быть >= 1'
    }
