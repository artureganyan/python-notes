# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Copyright (c) 2015 Artur Eganyan
#
# This work is provided "AS IS", WITHOUT ANY WARRANTY, express or implied.
#-------------------------------------------------------------------------------

# Кратко:
# - итерируемый объект - это объект (обычно контейнер), у которого есть итератор
# - итератор - это объект, используемый для перебора элементов контейнера
# - итератор имеет метод next(), который возвращает очередной элемент или генерирует исключение StopIteration
# - цикл for берет у контейнера итератор и проходит по всем элементам
# - генератор - это способ создания итератора в виде функции, содержащей инструкцию yield


# Перебор элементов контейнера (последовательности, множества, словаря и т.п.)
# обычно делается циклом for <элемент> in <контейнер>. Выражение <контейнер>
# вычисляется один раз и должно возвращать итерируемый объект (iterable object).
# 
# Итерируемый объект - это объект, поддерживающий метод __iter__(), который
# возвращает итератор. Итератор - это объект, используемый для перебора
# элементов контейнера и поддерживающий методы __iter__() и next(). __iter__()
# должен возвращать сам итератор, next() должен возвращать очередной элемент
# контейнера или генерировать исключение StopIteration, если элемента нет.
#
# Цикл получает итератор контейнера, и с его помощью проходит по всем
# элементам, присваивая очередной элемент в переменную <элемент>. После цикла
# переменная не удаляется (но если контейнер был пустым, она может быть и
# не создана). Внутри цикла переменную можно менять - при следующей итерации
# она все равно будет ссылаться на очередной элемент.
#
# Замечание: Итератор имеет метод __iter__(), поэтому сам является итерируемым
# объектом и может использоваться там, где требуется контейнер (например, в 
# цикле for). Однако если где-то один контейнер используется несколько раз
# (например, в нескольких циклах for), то для него каждый раз будет создаваться
# новый итератор. А если там же передавать не контейнер, а итератор, он не
# будет сбрасываться в начальное состояние и может достигнуть конца контейнера
# уже после первого цикла.


for e in ['a', 'b', 'c']:                 # Перебор элементов будет сделан через итератор ['a', 'b', 'c'].__iter__()
    print e                               # a, b, c

for i, e in enumerate(['a', 'b', 'c']):   # enumerate() возвращает итератор, идущий по парам (индекс, элемент)
    print i, e                            # 0 a, 1 b, 2 c

for e in reversed(['a', 'b', 'c']):       # reversed() возвращает итератор, идущий с конца к началу
    print e                               # c, b, a

for k, v in {'a':1, 'b':2}.iteritems():   # iteritems() возвращает итератор, идущий по парам (ключ, значение) 
    print k, v                            # a 1, b 2

for e in {'a':1, 'b':2}.iteritems():      # То же самое, но просто пары (ключ, значение) будут присвоены в e
    print e                               # ('a', 1), ('b', 2)


# Простой пример контейнера и его итератора
class MyContainer:

    def __init__( self ):
        self.data = []

    def add( self, e ):
        self.data.append(e)

    def __iter__( self ):
        return MyContainerIterator(self)

class MyContainerIterator:

    def __init__( self, container ):
        self.c = container
        self.i = 0

    def __iter__( self ):
        return self

    def next( self ):
        if self.i < len(self.c.data):
            e = self.c.data[self.i]
            self.i += 1
            return e
        else:
            raise StopIteration

c = MyContainer()
c.add(1)
c.add(2)
c.add(3)

for e in c:
    print e  # 1 2 3


# Удобная функция iter() возвращает итератор для переданного в нее объекта.
# Для итерируемых объектов она возвращает объект.__iter__(). Для объектов,
# поддерживающих обращение по индексу (объект[i]), она возвращает специальный 
# итератор. Также она может создать итератор, возвращающий значения 
# пользовательской функции (см. ниже).

a = [0, 1, 2, 3, 4, 5]
for e in iter(a.pop, 0): # Итератор будет возвращать a.pop(), пока не получит 0
    print e              # 5 4 3 2 1


# Генератор - это итератор, созданный с помощью функции, содержащей инструкцию 
# yield. При первом вызове такая функция возвращает итератор. Каждый вызов 
# итератор.next() будет выполнять функцию до инструкции "yield <значение>", на 
# которой она остановится, и возвращать <значение>. Если функция завершится, 
# достигнув конца, то будет сгенерировано исключение StopIteration.

from random import randint

def randomItem( data ):
    while len(data):
        yield data.pop(randint(0, len(data) - 1))

a = [1, 2, 3, 4, 5]
for e in randomItem(a):
    print e  # Числа из a в случайном порядке

# Если использовать генератор вручную, это выглядит так
a = [1, 2, 3]
i = randomItem(a)  # Создаст и вернет генератор
i.next()           # Выполнит функцию до yield и вернет него значение
i.next()           # -//-
i.next()           # -//-
try:
    i.next()       # Функция завершится, будет сгенерировано исключение StopIteration
except:
    print u"Функция randomItem() завершилась"


# Генератор можно создать с помощью generator expression, по аналогии с list 
# comprehension. Суть та же, только используются круглые скобки, и вместо 
# элемента списка указывается очередное возвращаемое значение:
#
# (<возвращаемое значение> for ... <for ...|if ...> ...)
#
# Эта запись эквивалента коду:
#
# def generator():
#     for ...
#         for ... | if ...
#             yield <возвращаемое значение>

a = [1, 2, 3, 4, 5]

# Генератор "e * 2 for e in a" передается в функцию-конструктор списка
print list(e * 2 for e in a)

# Тот же самый генератор
def nextItem(a):
    for e in a:
        yield e * 2

print list(nextItem(a))


# У генератора есть несколько методов, которых нет у обычного итератора.
#
# send(значение) - работает как next(), но при этом yield, на котором 
# остановилась функция, получит указанное значение и потом вернет его в 
# коде функции.
#
# throw(исключение) генерирует исключение в месте остановки функции, а потом 
# возвращает очередное значение yield, если функция до него дошла, или 
# генерирует исключение, вышедшее из функции.
#
# close() генерирует исключение GeneratorExit в месте остановки функции.
# Если функция его не перехватит или сгенерирует StopIteration, генератор
# просто завершится, а иначе он сгенерирует RuntimeError (например, если
# выполнится очередной yield).

def replaceItem(a):
    for i in range(len(a)):
        a[i] = yield a[i]

try:
    a = [1, 2, 3]
    i = replaceItem(a)  # Создаст и вернет генератор
    i.next()   # Остановится на a[0] = yield a[0], вернет a[0]
    i.send(0)  # Передаст в yield значение 0, продолжит выполнение с a[0] = 0,
               # вернет следующий yield (a[1])
    i.send(0)  # -//-: a[1] = 0, вернет a[2]
    i.send(0)  # -//-: a[2] = 0, сгенерирует StopIteration
except:
    pass
print a        # [0, 0, 0]
