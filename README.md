
# PyPoker

Игра про Покер, написанная на языке Python (*CPython 3.10*) и Prolog (*SWI-Prolog 8.4.3*).

⚠️***Может не работать на других версиях SWI-Prolog***⚠️

# Содержание

1) [Описание целей проекта](#описание-целей-проекта)
2) [Процесс разработки](#процесс-разработки)
    - [Графический интерфейс (GUI)](#графический-интерфейс-gui)
    - [Многопоточность (библиотека Threading)](#многопоточность-библиотека-threading)
    - [Основные элементы логики игры](#основные-элементы-логики-игры)
    - [Искусственный интеллект](#искусственный-интеллект)
    - [Тестирование](#тестирование)
3) [Результат](#результат)

# Описание целей проекта

Целью проекта было написание игры про покер с наличием простого и понятного графического интерфейса, а так же создание искусственного интеллекта (соперников-ботов)
на логическом языке программирования SWI-Prolog.


# Процесс разработки

- ### Графический интерфейс (GUI)

Для достижения поставленных целей был использован язык программирования Python из-за своей простоты и возможности быстрого написания кода,
а так же наличия встроенное библиотеки Tkinter.

Tkinter - библиотека позволяющая создать простой графический интерфейс для десктопных программ. Tkinter был выбран в силу своей простоты и хорошей совместимости.
Так как данная библиотека поставляется вместе с CPython как встроенная (built-in), это позволяет избавиться от лишних зависимостей в проекте.
Данная библиотека отлично подошла для реализации проекта из-за наличия внутри всех нужных компонентов (виджетов).

Для реализации GUI мог быть выбран PyGame (сторонняя библиотека для создания игр), но она оказалась хуже из-за отсутствия нужного количества виджетов (в PyGame, 
по умолчанию, нет виджета для кнопки).

- ### Многопоточность (библиотека Threading)

Для правильной работы игры, было необходимо реализовать многопоточность: элементы GUI должны иметь возможность обновляться по ходу игры, что не предусмотрено
в библиотеке Tkinter. Для реализации этой цели была использована библиотека theading, которая является встроенной в CPython.
Благодаря этой библиотеки игра происходит в следующем виде: 
* *в основном потоке происходит выполнение логики игры, которая представляет собой бесконечный цикл
ходов, до завершения игры.* 
* *в дополнительно открытом потоке, с помощью threading, происходит выполнение работы интерфейса и постоянное обновление окна игры.*

Благодаря такой структуре удается избежать конфликтов логики игры с интерфейсом и получить высокую отзывчивость GUI на действия игрока.

- ### Основные элементы логики игры

Для реализации логики игры, без использования сторонних библиотек на Python, были написаны классы для игральных карт, игровых столов, игроков, очереди игроков и т. д.
А также реализовано множество алгоритмов для определения комбинаций и их сравнения со всеми тонкостями игры в покер, а именно Техасский Холдем.

- ### Искусственный интеллект

Для реализации ИИ на языке Prolog был написан файл **ai.pl**, содержащий в себе функции, включающие элементы случайности, для реализации логики соперников.
Функции отвечают за действия ботов во время каждой стадии игры, а именно за принятия таких решений, как например: поставить деньги или сбросить карты?
повысить ставку или пропустить ход? уравнять ставку или сбросить карты? и т.д. для **каждого** этапа игры, которых в покере насчитывается четыре: 
* *Префлоп*
* *Флоп*
* *Терн*
* *и Ривер*.

- ### Тестирование

Для избежания семантический ошибок во время разработки, был написан модуль для тестирования внутренних функций, отвечающих за определение комбинаций
и сравнения рук игроков.

# Результат

Проект был реализован. Все поставленные цели были выполнены.

> **Начало раунда**
> 
> <img src="https://user-images.githubusercontent.com/29519431/208136932-6e092f7d-bf53-4b8c-861e-10fdd55914e2.png" alt="poker-screenshot-1" width="700"/>


> **Середина раунда**
> 
> <img src="https://user-images.githubusercontent.com/29519431/208137767-26de0e58-404c-4f3c-a0f2-ca7b4e79044e.png" alt="poker-screenshot-2" width="700"/>

> **Конец раунда**
> 
> <img src="https://user-images.githubusercontent.com/29519431/208138107-090c966b-418b-47a1-a04a-3acd4e900e4f.png" alt="poker-screenshot-3" width="700"/>
