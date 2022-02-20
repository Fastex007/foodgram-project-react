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
    SelfSubscribing = 1
    AllReadySubscribed = 2
    SelfUnsubscribing = 3
    AllReadyUnsubscribed = 4
    NoIngredients = 5
    NotUniqueIngredients = 6
    NoIngredientCount = 7
    RecepieAllReadyContainsInList = 8
    RecepieAllReadyRemoved = 9
    MinCookingTime = 10
    MinIngredientsCount = 11

    _titles = {
        SelfSubscribing: 'Вы не можете подписываться на самого себя',
        AllReadySubscribed: 'Вы уже подписаны на данного пользователя',
        SelfUnsubscribing: 'Вы не можете отписываться от самого себя',
        AllReadyUnsubscribed: 'Вы уже отписались от данного пользователя',
        NoIngredients: 'Не выбрано ни одного ингридиента',
        NotUniqueIngredients: 'Данный ингридиенет уже выбран',
        NoIngredientCount: 'Не указано количество',
        RecepieAllReadyContainsInList: 'Рецепт уже добавлен в список',
        RecepieAllReadyRemoved: 'Рецепт уже удален',
        MinCookingTime: 'Время приготовления должно быть >= 1 минут',
        MinIngredientsCount: 'Минимальное ингридиентов должно быть >= 1'
    }
