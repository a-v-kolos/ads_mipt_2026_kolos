# 1. Сделать реверс односвзяного списка.
# Пример: 
# Входные данные: 1, 2, 3, 4, 5
# Результат: 5, 4, 3, 2, 1

# сложность по памяти: O(1) потому что мы ничего никуда не копируем
# сложность по времени: O(n) потому что надо пройтись по n элементам


data = [1, 2, 3, 4, 5]

# односвязный список
class ListNode: # нода - пустая ячейка односвязного списка 
     def __init__(self, val=0, next=None):
         self.val = val # через точку это типа поле (переменные, хранящиеся внутри класса)
         self.next = next # указатель на следущую ноду

class Solution: # мы не всегда используем конструктор классов, нам он не нужен в этом классе потому что он только для функций
    def reverseList(self, head: ListNode) -> ListNode: # возвращает ListNode
        prev = None # предыдущая нода (None потому что перед головой ничего нет)
        curr = head # нода, которая сейчас 

        while curr: # цикл до того момента пока curr не станет None
            nxt = curr.next # запоминаем следующий узел прежде чем разворачивать стрелку
            curr.next = prev # разворот стрелочки обращаемся к значению next внутри curr
            prev = curr # сдвинули prev вперед к текущей ноде
            curr = nxt # сдвигаем curr вперёд, переходим к той ноде, которую до этого сохранили в nxt

        return prev # возвращаем голову

def build_list(values): # строит список из питоновского списка, который массив
    dummy = ListNode() # заглушка перед головой
    tail = dummy # последняя нода, которая пока заглушка
    for v in values:
        tail.next = ListNode(v) # прицепляем новый узел с val=v в конец
        tail = tail.next # сдвигаем хвост на только что добавленную ноду
    return dummy.next # возвращаем настоящую голову после заглушки

def to_pylist(head): # возвращает обратно к виду питоновского списка, иначе мы распечаатаь не сможем
    result = []
    while head: # цикл до того момента пока head не станет None
        result.append(head.val)
        head = head.next
    return result

head = build_list(data)
print(to_pylist(head))                      # [1, 2, 3, 4, 5]

reversed_head = Solution().reverseList(head)
print(to_pylist(reversed_head))             # [5, 4, 3, 2, 1]
