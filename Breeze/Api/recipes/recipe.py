from typing import Any

from Api.recipes.ingredient_slot import IngredientSlot


class Recipe:
    def __init__(self, ingredient_slots: list[IngredientSlot]):
        self.ingredients_slots = ingredient_slots

    def to_database(self) -> dict[str, Any]:
        infos: dict[str, Any] = {}
        for ingredient_slot in self.ingredients_slots:
            infos[ingredient_slot.name] = ingredient_slot.to_database()
        return infos

    @classmethod
    def from_database(cls, infos: dict[str, Any]):
        ingredient_slots: list[IngredientSlot] = []
        for slot_name, slot_infos in infos.items():
            ingredient_slots.append(IngredientSlot.from_database(slot_name=slot_name, slot_infos=slot_infos))
        return cls(ingredient_slots=ingredient_slots)
