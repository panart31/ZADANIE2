# -*- coding: utf-8 -*-
"""Геометрические тела: иерархия классов на базе абстрактного класса."""

import math
from abc import ABC, abstractmethod

from geometry.materials import Material


class Body(ABC):
    """Абстрактное тело: объём, площадь поверхности, масса."""

    def __init__(self, material):
        self.material = material  # проверка через property

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        if not isinstance(value, Material):
            raise TypeError("материал должен быть экземпляром Material")
        self._material = value

    @property
    def mass(self):
        """Масса тела = плотность * объём."""
        return self._material.density * self.volume()

    @abstractmethod
    def volume(self):
        """Объём тела, м^3."""

    @abstractmethod
    def surface_area(self):
        """Площадь поверхности, м^2."""

    @abstractmethod
    def params_str(self):
        """Строка с размерами тела."""

    @classmethod
    def kind(cls):
        """Имя класса тела."""
        return cls.__name__

    def __repr__(self):
        return f"{self.kind()}({self.params_str()}, {self._material!r})"

    def __str__(self):
        return (f"{self.kind()} [{self.params_str()}], {self._material}: "
                f"V={self.volume():.4f} м^3, S={self.surface_area():.4f} м^2, "
                f"m={self.mass:.2f} кг")

    def __eq__(self, other):
        if not isinstance(other, Body):
            return NotImplemented
        return (self.kind(), self.params_str(), self._material) == \
               (other.kind(), other.params_str(), other.material)


class Parallelepiped(Body):
    """Прямоугольный параллелепипед со сторонами a, b, c."""

    def __init__(self, a, b, c, material):
        super().__init__(material)
        self.a = a  # запись идёт через property с проверкой
        self.b = b
        self.c = c

    # managed-атрибуты: общая проверка для всех сторон
    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = self._check(value)

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = self._check(value)

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        self._c = self._check(value)

    @staticmethod
    def _check(value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("размер должен быть числом")
        if value <= 0:
            raise ValueError("размер должен быть положительным")
        return float(value)

    def volume(self):
        return self._a * self._b * self._c

    def surface_area(self):
        return 2 * (self._a * self._b + self._b * self._c + self._a * self._c)

    def params_str(self):
        return f"a={self._a:g}, b={self._b:g}, c={self._c:g}"


class Tetrahedron(Body):
    """Правильный тетраэдр с ребром a."""

    def __init__(self, a, material):
        super().__init__(material)
        self.a = a

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = Parallelepiped._check(value)

    def volume(self):
        return self._a ** 3 / (6 * math.sqrt(2))

    def surface_area(self):
        return math.sqrt(3) * self._a ** 2

    def params_str(self):
        return f"a={self._a:g}"


class SolidOfRevolution(Body):
    """Промежуточный класс для тел вращения."""

    def __init__(self, r, material):
        super().__init__(material)
        self.r = r

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        self._r = Parallelepiped._check(value)

    def volume(self):
        return 4 / 3 * math.pi * self._r ** 3

    def surface_area(self):
        return 4 * math.pi * self._r ** 2

    def params_str(self):
        return f"r={self._r:g}"


class Sphere(SolidOfRevolution):
    """Шар радиуса r."""
