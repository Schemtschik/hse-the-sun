# How To Use

Все нижеописанные действия выполняются в командной строке.
На Windows и MacOS для работоспособности данной интрукции должны быть установлены Git и Python3.

## Установка

```
git clone https://github.com/Schemtschik/hse-the-sun.git
cd hse-the-sun
pip3 install -r requirments.txt
```
## Использование
Все команды имеют опцию `--help`, вывод которой приведён ниже.
Отдельное внимание стоит уделить опции `--raw`, которая переключает скрипты на вывод данных в упрощённом формате, в котором они могут быть легко использованы далее.
```
# Преобразуем формат файла в JSON
python3 raw_to_json.py data/rgousfull.txt data/rgousfull.json
# Переведём координаты из гелиоцентрической в геоцентрическую
python3 transform.py data/rgousfull.json data/rgousfull.hsc.json
# Построим график зависимости точности нахождения старых пятен от размера эллипса, чтобы определить оптимальный размер
python3 learn_second_appearance.py data/rgousfull.hsc.json
# Найдём долгоживущие пятна
python3 mark_second_appearance.py data/rgousfull.hsc.json data/rgousfull.marked.json
# Удалим лишние пятна с левого края, не трогая ранее найденные старые пятна
python3 filter_left.py data/rgousfull.marked.json data/rgousfull.filtered.json
```
## Man

```
Usage: raw_to_json.py [OPTIONS] INPUT_FILE OUTPUT_FILE

  Transforms raw data (format: data/rulesrgo.txt) to json structures
  implemented in common.py

Options:
  --help  Show this message and exit.
```

```
Usage: transform.py [OPTIONS] INPUT_FILE OUTPUT_FILE

  Transforms heliocentric coordinates to geocentric ones

Options:
  --help  Show this message and exit.
```

```
Usage: learn_second_appearance.py [OPTIONS] INPUT_FILE

  Draws the graph of accuracy by ellipse size

Options:
  --long INTEGER           searching ellipse longitude semi-axis in degrees (8
                           by default)
  --lat INTEGER            searching ellipse latitude semi-axis in degrees (5
                           by default)
  --time-interval INTEGER  searching time semi-range in hours (12 by default)
  --help                   Show this message and exit.
```

```
Usage: mark_second_appearance.py [OPTIONS] INPUT_FILE OUTPUT_FILE

  Marks long live sunspots

Options:
  --raw                    print just pairs "[old group id] [new group id]"
  --long INTEGER           searching ellipse longitude semi-axis in degrees (8
                           by default)
  --lat INTEGER            searching ellipse latitude semi-axis in degrees (5
                           by default)
  --time-interval INTEGER  searching time semi-range in hours (12 by default)
  --period INTEGER         searching period in days (15 by default)
  --area-limit INTEGER     minimal area of sunspot before disappearance (200
                           by default)
  --help                   Show this message and exit.
```

```
Usage: filter_left.py [OPTIONS] INPUT_FILE OUTPUT_FILE

  Filters extra sunspots on the left, taking care of long live sunspots

Options:
  --raw                      print ids of not filtered groups
  --angle-step INTEGER       angle frame size in degrees (5 by default)
  --area-step-low INTEGER    area frame size low (1 by default)
  --area-limit-low INTEGER   max area to process with low frame size (100 by
                             default)
  --area-step-high INTEGER   area frame size high (20 by default)
  --area-limit-high INTEGER  max area to process with high frame size (3600 by
                             default)
  --help                     Show this message and exit.
```
