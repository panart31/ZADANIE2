# -*- coding: utf-8 -*-
"""ЛР №2, вариант 16. Консольный интерфейс расчёта геометрических тел."""

from geometry import (Parallelepiped, Sphere, Tetrahedron,
                      available_materials, get_material,
                      ResultsDB, export_docx, export_xlsx)

MENU = """
--- Расчёт геометрических тел (вариант 16) ---
1 - Параллелепипед
2 - Тетраэдр
3 - Шар
4 - Показать сохранённые результаты
5 - Экспорт в docx
6 - Экспорт в xlsx
0 - Выход
"""


def read_positive(prompt):
    """Ввод положительного числа с повтором при ошибке."""
    while True:
        try:
            value = float(input(prompt).replace(",", "."))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Ошибка: нужно положительное число")


def read_material():
    """Выбор материала из справочника."""
    names = available_materials()
    print("Доступные материалы:", ", ".join(names))
    while True:
        try:
            return get_material(input("Материал: "))
        except KeyError as e:
            print(e.args[0])


def make_body(choice):
    """Создание тела по пункту меню."""
    material = read_material()
    if choice == "1":
        a = read_positive("Сторона a, м: ")
        b = read_positive("Сторона b, м: ")
        c = read_positive("Сторона c, м: ")
        return Parallelepiped(a, b, c, material)
    if choice == "2":
        a = read_positive("Ребро a, м: ")
        return Tetrahedron(a, material)
    return Sphere(read_positive("Радиус r, м: "), material)


def show_results(db):
    """Печать сохранённых результатов."""
    rows = db.all()
    if not rows:
        print("База данных пуста")
        return
    print(f"{'ID':<4}{'Тело':<16}{'Параметры':<26}{'Материал':<30}"
          f"{'V, м^3':>12}{'S, м^2':>12}{'m, кг':>12}")
    for id_, body, params, material, vol, area, mass, created in rows:
        print(f"{id_:<4}{body:<16}{params:<26}{material:<30}"
              f"{vol:>12.4f}{area:>12.4f}{mass:>12.4f}")
    print(f"Всего записей: {len(db)}")


def main():
    db = ResultsDB()
    while True:
        print(MENU)
        choice = input("Выберите пункт: ").strip()
        if choice == "0":
            print("Выход")
            break
        if choice in ("1", "2", "3"):
            try:
                body = make_body(choice)
            except (ValueError, TypeError) as e:
                print("Ошибка:", e)
                continue
            print(body)
            db.add(body)
            print("Результат сохранён в results.db")
        elif choice == "4":
            show_results(db)
        elif choice == "5":
            name = export_docx(db.all())
            print(f"Отчёт сохранён: {name}")
        elif choice == "6":
            name = export_xlsx(db.all())
            print(f"Таблица сохранена: {name}")
        else:
            print("Нет такого пункта меню")


if __name__ == "__main__":
    main()
