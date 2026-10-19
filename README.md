# Geometry Calc (ЛР №2, вариант 16)

Консольная программа для расчёта геометрических тел: параллелепипед,
тетраэдр и шар. Для выбранного тела и материала считаются объём, площадь
поверхности и масса, результат сохраняется в базу sqlite и выгружается
в отчёт docx или xlsx.

## Состав пакета geometry

- materials.py — справочник материалов (плотность, кг/м3)
- shapes.py — классы тел: абстрактный класс Body и наследники
- storage.py — база результатов sqlite3 и экспорт в docx/xlsx

## Запуск

Требуется Python 3.10+.

```
pip install -r requirements.txt
python main.py
```

## Тесты

```
pytest tests -v
```

## Запуск в Docker

```
docker build -t geometry-calc .
docker run -it geometry-calc
```

## Формулы

- параллелепипед: V = abc, S = 2(ab + bc + ac)
- правильный тетраэдр: V = a^3 / (6*sqrt(2)), S = sqrt(3) * a^2
- шар: V = 4/3 * pi * r^3, S = 4 * pi * r^2
- масса: m = плотность * V

Выполнены уровни сложности Rare, Medium и Well-done
(тесты pytest, хранение в sqlite3, Docker).
