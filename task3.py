# q1 — число вставок (append)
# q2 — число поисков (find)
# q3 — число вызовов print_tree
# q4 — число вызовов height
# n — текущее число узлов в дереве


# сложность по времени: O((q1 + q2)·log n + (q3 + q4)·n)
# сложность по памяти: O(q1 · log n) - вставки (append)


# СЛОЖНОСТЬ ПО ВРЕМЕНИ:
#   O(log n)        — append в среднем/худшем для RB-дерева: спуск по дереву (O(log n))
#                     + balance (перекраски O(log n), поворотов не более O(1) на итерацию,
#                     всего O(log n))
#   O(log n)        — find: спуск от корня до листа, каждый шаг отсекает половину
#   O(n)            — print_tree: обход всех n узлов (по одному print на узел)
#   O(n)            — height: рекурсивный обход всех узлов (max по двум поддеревьям)
#   ИТОГО: O(q1·log n + q2·log n + q3·n + q4·n) = O((q1+q2)·log n + (q3+q4)·n)
#
# СЛОЖНОСТЬ ПО ПАМЯТИ:
#   O(n)            — сами узлы дерева (по одному Node на каждую успешную вставку,
#                     плюс один NIL-сентинел)
#   O(1)            — NIL-сентинел (один узел на всё дерево)
#   O(log n)        — стек рекурсии balance (глубина ≤ высоты дерева = O(log n))
#   O(h) = O(log n) — стек рекурсии height / print_tree в худшем случае
#                     (h — высота RB-дерева, h = O(log n))
#   ИТОГО: O(n) — доминируют узлы дерева; вспомогательная память O(log n)
#   (стек рекурсии) не превышает O(n), но при подсчёте «чистой» дополнительной
#   памяти без учёта самих узлов — O(log n).



class Node:
    def __init__(self, value,  left=None, right=None, color='red'):
        self.value = value
        self.color = color
        self.left = left
        self.right = right
        self.parent = None

class Tree:
    def __init__(self):
        self.NIL = Node(value=None, color='black') #создаем узел-заглушку, всегда черный, т.к. листья черные
        self.NIL.left = self.NIL #ссылаем все на NIL, чтобы не делать 100500 проверок is None
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL

        self.root = self.NIL #пока в дереве ничего нет, корень NIL

    def append(self, value):  #по идее за log(n), потому что каждый раз отсекаем половину
        new_node = Node(value, color='red') #создаем новый узел, по правилу он всегда красный
        new_node.left = self.NIL
        new_node.right = self.NIL
        new_node.parent = self.NIL

        parent = self.NIL           # родитель будущего узла
        current = self.root         # текущий узел, начинаем смотреть с корня
        while current is not self.NIL: #пока не дойдем до пустоты
            parent = current #помним последний реальный узел
            if value < current.value:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent #последний реальный узел становится родителем
        if parent is self.NIL: #возможно только если дерево было пустое
            self.root = new_node
        elif value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        self.balance(new_node)


    def rotation(self, node, direction):
        if direction == 'left':   # Левый поворот: правый ребёнок узла становится на его место, левый внук переездает к деду
            child = node.right                  # будущий корень
            node.right = child.left             # правое поддерево перевешиваем к узлу, вокруг которого поворот
            if child.left is not self.NIL:
                child.left.parent = node
            child.parent = node.parent          # переставляем правого ребенка на место узла, вокруг которого поворот
            if node.parent is self.NIL:
                self.root = child               # возможно это корень всего дерева
            elif node is node.parent.left:     # если нет, то новый корень поддерева подвешиваем туда, где висел узел, вокруг которого мы поворачивали
                node.parent.left = child
            else:
                node.parent.right = child
            child.left = node                   # узел, вокруг которого поворачивали, становится левым ребенком своего парвого ребенка
            node.parent = child
            return child

        else:  # если поворот направо, то левый ребенок узла встанет на его место
            child = node.left
            node.left = child.right
            if child.right is not self.NIL:
                child.right.parent = node
            child.parent = node.parent
            if node.parent is self.NIL:
                self.root = child
            elif node is node.parent.left:
                node.parent.left = child
            else:
                node.parent.right = child
            child.right = node
            node.parent = child
            return child


    def balance(self, node):
        while node.parent.color == 'red': #вставили новый красныц узел и его родитель тоже красный
            parent = node.parent
            grandparent = parent.parent

            if parent is grandparent.left: #новый узел добавили слева от деда
                uncle = grandparent.right

                if uncle.color == 'red': #если дядя красный - перекрашиваем без поворота
                    parent.color = 'black'
                    uncle.color = 'black'
                    grandparent.color = 'red'
                    node = grandparent        # проверяем узлы выше

                else: #дядя черный
                    if node is parent.right: #новый узел справа
                        node = parent
                        self.rotation(node, 'left')   #новый узел становится корнем, а родитель левым ребенком
                        parent = node.parent

                    parent.color = 'black' #перекрашиваем отца
                    grandparent.color = 'red' #перекрашиваем деда
                    self.rotation(grandparent, 'right') #правый поворот вокруг дедушки

            else:        # Наоборот, новый узел добавлен справа от деда
                uncle = grandparent.left

                if uncle.color == 'red': #только перекрашиваем
                    parent.color = 'black'
                    uncle.color = 'black'
                    grandparent.color = 'red'
                    node = grandparent

                else:
                    if node is parent.left: #если узел был добавлен слева, то это зигзаг, который надо распрямить правым поворотом вокруг отца
                        node = parent
                        self.rotation(node, 'right')
                        parent = node.parent

                    parent.color = 'black' #перекрашиваем отца
                    grandparent.color = 'red' #перекрашиваем деда
                    self.rotation(grandparent, 'left') #левы1й поворот вокруг деда

        self.root.color = 'black'


    def print_tree(self, node=None, indent=0): #вывод дерева горизонтально, отступы показывают вложенность, o(n) выводим все узлы
        if node is None:
            node = self.root
        if node is self.NIL:
            return
        self.print_tree(node.right, indent + 1) #правое наверху, каждый слой indent+1, таким образом отделяем слои
        print("      " * indent + str(node.value) + node.color[0]) #пишем узел и цвет
        self.print_tree(node.left, indent + 1) #левое поддерево внизу

    def find(self, value):    #по идее за log(n), потому что каждый раз отсекаем половину
        node = self.root #начинаем поиск с корня
        while node is not self.NIL: #пока не дошли до листьев
            if value == node.value:
                return True
            if value < node.value:
                node = node.left
            else:
                node = node.right
        return False


    def height(self, node=None):
        if node is None:
            node = self.root
        if node is self.NIL:
            return 0
        return max(self.height(node.left), self.height(node.right)) + (node.color == 'black')


t = Tree()
for x in [10, 20, 30, 15, 25, 5, 1, 40, 50, 35]:
    t.append(x)
t.print_tree()

print(t.find(25))
print(t.find(99))

print("height =", t.height())
print("-----------------------------------------------------------------------------")
for x in [11, 17, 21, 2, 36, 70]:
    t.append(x)
t.print_tree()
print("height =", t.height())
