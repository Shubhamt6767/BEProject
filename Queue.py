queue = []
dic = {1: 'enqueue()', 2: 'dequeue()', 3: 'show()'}
print("1 : add\n2 : remove\n3 : display\n4 : exit")

choice = int(input("Enter the choice : "))
def enqueue():
    data = input("Enter the element  : ")
    queue.append(data)
    print(data," is added in queue")

def dequeue():
    if not queue:
        print("Queue is empty!")
    else:
        val = queue.pop(0)
        print(val," is removed")

def show():
    if not queue:
        print("Queue is empty!")
    else:
        print(queue)


print(type(dic[choice]))




