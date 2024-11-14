import threading

lock = threading.Lock()
shared_val = [0]  # 使用列表来包装整数，以便通过引用传递


def print1(val_list):
    lock.acquire()
    val_list[0] += 1  # 修改列表中的元素
    print(val_list[0])
    lock.release()


def print2(val_list):
    lock.acquire()
    val_list[0] += 1
    print(val_list[0])
    lock.release()


if __name__ == "__main__":
    for i in range(50):
        t1 = threading.Thread(target=print1, args=(shared_val,))
        t2 = threading.Thread(target=print2, args=(shared_val,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    print("hello world")