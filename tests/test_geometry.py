# -*- coding: utf-8 -*-
"""Тесты пакета geometry."""

import math
import os
import sys
from abc import ABC

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from geometry import (Material, Parallelepiped, Sphere, Tetrahedron,
                      get_material, ResultsDB, export_docx, export_xlsx)
from geometry.shapes import Body, SolidOfRevolution


def steel():
    return get_material("сталь")


class TestMaterial:
    def test_preset_density(self):
        assert steel().density == 7850

    def test_str(self):
        assert "сталь" in str(steel())

    def test_invalid_density(self):
        with pytest.raises(ValueError):
            Material("мел", -5)

    def test_invalid_name(self):
        with pytest.raises(ValueError):
            Material("  ", 100)

    def test_unknown_material(self):
        with pytest.raises(KeyError):
            get_material("неон")

    def test_eq(self):
        assert steel() == get_material("сталь")


class TestParallelepiped:
    def test_volume_and_area(self):
        p = Parallelepiped(2, 3, 4, steel())
        assert p.volume() == 24
        assert p.surface_area() == 2 * (6 + 12 + 8)

    def test_mass(self):
        p = Parallelepiped(1, 1, 1, steel())
        assert p.mass == pytest.approx(7850)

    def test_invalid_side(self):
        with pytest.raises(ValueError):
            Parallelepiped(1, 0, 2, steel())

    def test_side_setter_validates(self):
        p = Parallelepiped(1, 1, 1, steel())
        with pytest.raises(ValueError):
            p.a = -3

    def test_str_and_repr(self):
        p = Parallelepiped(2, 2, 2, steel())
        assert "Parallelepiped" in str(p)
        assert "Material" in repr(p)

    def test_eq(self):
        assert Parallelepiped(1, 2, 3, steel()) == Parallelepiped(1, 2, 3, steel())


class TestTetrahedron:
    def test_volume(self):
        t = Tetrahedron(2, steel())
        assert t.volume() == pytest.approx(8 / (6 * math.sqrt(2)))

    def test_area(self):
        t = Tetrahedron(2, steel())
        assert t.surface_area() == pytest.approx(math.sqrt(3) * 4)


class TestSphere:
    def test_volume(self):
        s = Sphere(1, steel())
        assert s.volume() == pytest.approx(4 / 3 * math.pi)

    def test_area(self):
        s = Sphere(3, steel())
        assert s.surface_area() == pytest.approx(4 * math.pi * 9)

    def test_hierarchy(self):
        assert issubclass(Sphere, SolidOfRevolution)
        assert issubclass(SolidOfRevolution, Body)
        assert issubclass(Body, ABC)


class TestBody:
    def test_abstract_cannot_instantiate(self):
        with pytest.raises(TypeError):
            Body(steel())

    def test_material_type_checked(self):
        with pytest.raises(TypeError):
            Sphere(1, "сталь")


class TestStorage:
    def test_add_and_read(self, tmp_path):
        db = ResultsDB(str(tmp_path / "test.db"))
        db.add(Parallelepiped(1, 2, 3, steel()))
        db.add(Sphere(1, steel()))
        assert len(db) == 2
        rows = list(db)
        assert rows[0][1] == "Parallelepiped"
        assert rows[1][1] == "Sphere"
        assert rows[0][5] == pytest.approx(2 * (2 + 6 + 3))

    def test_clear(self, tmp_path):
        db = ResultsDB(str(tmp_path / "test.db"))
        db.add(Tetrahedron(1, steel()))
        db.clear()
        assert len(db) == 0

    def test_export_docx(self, tmp_path):
        db = ResultsDB(str(tmp_path / "test.db"))
        db.add(Sphere(2, steel()))
        name = export_docx(db.all(), str(tmp_path / "r.docx"))
        assert os.path.getsize(name) > 0

    def test_export_xlsx(self, tmp_path):
        db = ResultsDB(str(tmp_path / "test.db"))
        db.add(Sphere(2, steel()))
        name = export_xlsx(db.all(), str(tmp_path / "r.xlsx"))
        assert os.path.getsize(name) > 0
