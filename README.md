
### Name

<!-- Simple-diet - is a small console utility that contains a food diary for calorie tracking and a sports assistant simple-sport. -->
Simple-diet - небольшая консольная утилита, позволяющая вести дневник калорий и выполнять интервальные тренировки

### Synopsis

Использование: 
    
    ./main.py

Для тренировки:

    ./ss.py -i

    ./ss.py -f [файлы тренировок]

<!-- Usage: ./simple-diet.py -->

<!-- Usage: ./simple-sport.py -f [files] -->

### Description

Программа хранит данные о пользователях и их дневники питания в базе данных. 

На основе пользовательской информации происодит подсчет суточной нормы калорий, а на основе дневника - подсчет уже полученных калорий.

Спортивный ассистент, на данный момент, использует файлы с тренировками.

Возможен запуск в интерактивном режиме, когда предлагается выбрать существующую программу из директории 'basics', или запуск с передачей файлов напрямую.

<!-- A food diary allows you to track the amount you eat during the day. It calculates your daily calorie intake and the caloric value of all foods eaten. Food diary uses SQLite to store its data. -->

<!-- The sports assistant allows you to create training programs and carry them out according to a timer. For creating new training file you can use every text editor you like. See *File format* section below. -->

### File format

Файлы тренировок для спортивного ассистента должны быть созданы вручную с соблюдением определенного синтаксиса. Для упрощения, в каталоге с программой находится файл 'tss.vim', включающий подсветку синтаксиса для Vim. Рекомендуется сохранять файлы с раширением '\*.tss' в директории 'basics'.

Пример синтаксиса файла тренировки:

    # Название тренировки
    name='Warm-up'
    # Продолжительность пауз
    pause=5s
    # Отдых между повторами
    relax=0s
    # Количество повторов
    repiats=1
    # Пауза между тренировками
    on_end=10s

    # Символ '|' может быть использован для указания алтернативных упражнений
    ex1|ex2:30s
    # Разделителем между названия упражнения и его продолжительностью может быть как символ ':' так и '->'
    ex2|ex5->0.5m
    # Продолжительность упражнения указывается в виде числа, тогда оно будет измеряться в секундах, или чиса с модификатором времени
    ex3->40s
    ex5:1m

<!-- In the new version, the exercise file contains all the necessary data to build a workout plan: the number of repeats, time intervals and the set of exercises itself. The files have the extension '.tss'. -->

<!-- The grid symbol ( # ) is used to create comments, empty lines will skip. -->

<!-- The execution time must be specified with a time modifier (s or m), the separator for the exercises is either a colon symbol ( : ) or a small arrow ( -> ). -->

<!-- The same principle is used to set parameters, but the separator is the equality symbol ( = ). If the parameter is set by a simple number, like the number of approaches, then the time modifier cannot be set. -->

<!-- The vertical line symbol '|' makes it possible to randomly select an exercise. -->

    <!-- name='Warm-up' -->
    <!-- pause=5s -->
    <!-- relax=0s -->
    <!-- repiats=1 -->
    <!-- on\_end=10s -->

    <!-- ex1|ex2|ex3:30s -->
    <!-- ex2|ex5->0.5m -->
    <!-- ex3->40s -->
    <!-- ex5:1m -->

