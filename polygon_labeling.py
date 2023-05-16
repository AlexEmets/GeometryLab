from math import sqrt
import time

try:
    # Python3
    from queue import PriorityQueue
    from math import inf
except ImportError:
    # Python2
    from Queue import PriorityQueue

    inf = float("inf")

# Ці функції пов'язані з обчисленням відстані між точкою (x, y) і полігоном, представленим списком вершин. Ось їх пояснення:

# Функція _point_to_polygon_distance(x, y, polygon) обчислює відстань від точки (x, y) до полігону. 
# Вона використовує алгоритм "найближчої точки" для обчислення цієї відстані. 
# Внутрішній цикл перебирає всі сегменти полігону, обчислює відстань від точки до кожного сегмента за допомогою функції _get_seg_dist_sq, 
# і зберігає найменшу відстань. Якщо точка (x, y) знаходиться всередині полігону, функція повертає позитивне значення відстані. 
# Якщо точка знаходиться ззовні полігону, функція повертає від'ємне значення відстані.



def _point_to_polygon_distance(x, y, polygon):
    inside = False
    min_dist_sq = inf

    b = polygon[-1]
    for a in polygon:

        if ((a[1] > y) != (b[1] > y) and
                (x < (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) + a[0])):
            inside = not inside

        min_dist_sq = min(min_dist_sq, _get_seg_dist_sq(x, y, a, b))
        b = a

    result = sqrt(min_dist_sq)
    if not inside:
        return -result
    return result

# Функція _get_seg_dist_sq(px, py, a, b) обчислює квадрат відстані від точки (px, py) до сегмента, 
# який заданий вершинами a і b. Ця функція використовує проекцію точки (px, py) на сегмент і обчислює відстань до цієї проекції. 
# Вона використовується в _point_to_polygon_distance для обчислення відстані до кожного сегмента полігону.

# Загальна ідея цих функцій полягає в тому, щоб знайти найближчу відстань між точкою і полігоном, 
# щоб визначити, чи знаходиться точка всередині полігону або ззовні нього.
def _get_seg_dist_sq(px, py, a, b):
    x = a[0]
    y = a[1]
    dx = b[0] - x
    dy = b[1] - y

    if dx != 0 or dy != 0:
        t = ((px - x) * dx + (py - y) * dy) / (dx * dx + dy * dy)

        if t > 1:
            x = b[0]
            y = b[1]

        elif t > 0:
            x += dx * t
            y += dy * t

    dx = px - x
    dy = py - y

    return dx * dx + dy * dy


class Cell(object):
    def __init__(self, x, y, h, polygon):
        self.h = h
        self.y = y
        self.x = x
        self.d = _point_to_polygon_distance(x, y, polygon)
        self.max = self.d + self.h * sqrt(2)

    def __lt__(self, other):
        return self.max < other.max

    def __lte__(self, other):
        return self.max <= other.max

    def __gt__(self, other):
        return self.max > other.max

    def __gte__(self, other):
        return self.max >= other.max

    def __eq__(self, other):
        return self.max == other.max

# Функція _get_centroid_cell(polygon) обчислює центроїд полігона. Вона використовує формулу Гауса для обчислення центроїда. 
# У циклі обчислюється сума координат x та y, множена на фактор f, а також сума площ полігону, де f - це підполігон, 
# який визначається вершинами a та b. В результаті центроїд обчислюється як середнє значення координат x та y, 
# поділене на суму площ полігону.
def _get_centroid_cell(polygon):
    area = 0
    x = 0
    y = 0
    b = polygon[-1]  # prev
    for a in polygon:
        f = a[0] * b[1] - b[0] * a[1]
        x += (a[0] + b[0]) * f
        y += (a[1] + b[1]) * f
        area += f * 3
        b = a
    if area == 0:
        return Cell(polygon[0][0], polygon[0][1], 0, polygon)
    return Cell(x / area, y / area, 0, polygon)

    pass

# Функція polylabel(polygon, precision=1.0, debug=False, with_distance=False) знаходить точку полігону з найбільшою відстанню до країв 
# (якщо ця відстань є достатньою) за допомогою алгоритму полігонової мітки. 
# Спочатку обчислюється охоплюючий прямокутник (bounding box) для полігона, 
# а потім визначається розмір комірки на основі ширини та висоти цього прямокутника. 
# Далі створюється черга комірок (cell_queue), яка починається від лівого верхнього кута охоплюючого прямокутника 
# та містить комірки з півкоординатами та розміром комірки. Комірки в черзі сортуються 
# за їх максимальним значенням d - відстанню до країв полігона
def polygon_labeling(polygon, precision=1.0, debug=False, with_distance=False):
    # find bounding box
    first_item = polygon[0]
    min_x = first_item[0]
    min_y = first_item[1]
    max_x = first_item[0]
    max_y = first_item[1]
    for p in polygon:
        if p[0] < min_x:
            min_x = p[0]
        if p[1] < min_y:
            min_y = p[1]
        if p[0] > max_x:
            max_x = p[0]
        if p[1] > max_y:
            max_y = p[1]

    width = max_x - min_x
    height = max_y - min_y
    cell_size = min(width, height)
    h = cell_size / 2.0

    cell_queue = PriorityQueue()

    if cell_size == 0:
        if with_distance:
            return [min_x, min_y], None
        else:
            return [min_x, min_y]

    # cover polygon with initial cells
    x = min_x
    while x < max_x:
        y = min_y
        while y < max_y:
            c = Cell(x + h, y + h, h, polygon)
            y += cell_size
            cell_queue.put((-c.max, time.time(), c))
        x += cell_size

    best_cell = _get_centroid_cell(polygon)

    bbox_cell = Cell(min_x + width / 2, min_y + height / 2, 0, polygon)
    if bbox_cell.d > best_cell.d:
        best_cell = bbox_cell

    num_of_probes = cell_queue.qsize()
    while not cell_queue.empty():
        _, __, cell = cell_queue.get()

        if cell.d > best_cell.d:
            best_cell = cell

            if debug:
                print('found best {} after {} probes'.format(
                    round(1e4 * cell.d) / 1e4, num_of_probes))

        if cell.max - best_cell.d <= precision:
            continue

        h = cell.h / 2
        c = Cell(cell.x - h, cell.y - h, h, polygon)
        cell_queue.put((-c.max, time.time(), c))
        c = Cell(cell.x + h, cell.y - h, h, polygon)
        cell_queue.put((-c.max, time.time(), c))
        c = Cell(cell.x - h, cell.y + h, h, polygon)
        cell_queue.put((-c.max, time.time(), c))
        c = Cell(cell.x + h, cell.y + h, h, polygon)
        cell_queue.put((-c.max, time.time(), c))
        num_of_probes += 4

    if debug:
        print('num probes: {}'.format(num_of_probes))
        print('best distance: {}'.format(best_cell.d))
    if with_distance:
        return [best_cell.x, best_cell.y], best_cell.d
    else:
        return [best_cell.x, best_cell.y]

# складність алгоритму

# Складність алгоритму polylabel, який використовується для пошуку максимального вписаного кола в полігон, може бути оцінена як O(nlogn), де n - кількість вершин полігона.

# Алгоритм polylabel складається з наступних етапів:

# Знаходження охоплюючого прямокутника (bounding box): Цей етап вимагає пройти по всіх вершинах полігона, що займає O(n) часу.

# Покриття полігона початковими комірками: В цьому етапі створюється черга комірок з півкоординатами та розміром комірки. Кількість початкових комірок залежить від розміру полігона та розміру комірки. За умови, що розмір полігона складає O(n), а розмір комірки є сталою, кількість початкових комірок також є O(n).

# Визначення найкращої комірки: У цьому етапі використовується черга пріоритетів, де вибирається комірка з найбільшим значенням d (відстань від точки до полігона). Кількість комірок у черзі залежить від точності (precision) та відносної відстані між комірками. В худшому випадку, коли точність є достатньою і відстань між комірками є сталою, кількість комірок у черзі складатиме O(n). Кожне видалення комірки з черги потребує O(logn) часу.

# Розділення комірок: У цьому етапі комірки розділяються на менші комірки та додаються до черги комірок. Кількість нових комірок, які додаються до черги, залежить від кількості комірок, які потрібно розділити, тобто від кількості комірок у черзі. В худшому випадку, кількість комірок, які додаються додаються до черги, може бути порівняна з кількістю комірок, які вже знаходяться в черзі. Таким чином, в худшому випадку, кількість комірок у черзі може зростати пропорційно кількості комірок, які були додані до черги в попередніх етапах. Оскільки всі комірки в полігоні мають відстань від країв полігона, цей показник також може бути порівняний з кількістю вершин полігона.

# Таким чином, загальна складність алгоритму polylabel може бути оцінена як O(nlogn), де n - кількість вершин полігона. За умови, що кількість вершин полігона складає O(n) і кожен етап алгоритму виконується ефективно, алгоритм polylabel займе O(nlogn) часу.

# Варто зазначити, що це оцінка теоретичної складності, і фактичний час виконання може залежати від реалізації алгоритму, розміру та форми полігона, а також від точності, заданої в якості параметра.