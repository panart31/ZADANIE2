# -*- coding: utf-8 -*-
"""Справочник материалов: плотности в кг/м^3."""

DENSITY_TABLE = {
    "сталь": 7850,
    "алюминий": 2700,
    "титан": 4506,
    "медь": 8960,
    "дуб": 750,
    "гранит": 2600,
    "лёд": 917,
    "пробка": 240,
}


class Material:
    """Материал с контролируемой плотностью (managed attribute)."""

    def __init__(self, name, density):
        self.name = name
        self.density = density  # проверка через property

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("название материала не может быть пустым")
        self._name = value.strip()

    @property
    def density(self):
        return self._density

    @density.setter
    def density(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("плотность должна быть положительным числом")
        self._density = float(value)

    def __str__(self):
        return f"{self._name} (плотность {self._density:g} кг/м^3)"

    def __repr__(self):
        return f"Material({self._name!r}, {self._density})"

    def __eq__(self, other):
        if not isinstance(other, Material):
            return NotImplemented
        return (self._name.lower(), self._density) == (other.name.lower(), other.density)


def get_material(name):
    """Материал по названию из справочника."""
    key = name.strip().lower()
    if key not in DENSITY_TABLE:
        raise KeyError(f"материал '{name}' отсутствует в справочнике")
    return Material(key, DENSITY_TABLE[key])


def available_materials():
    """Список доступных материалов."""
    return list(DENSITY_TABLE)
