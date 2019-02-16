import threading

import numpy as np

mutex_w = threading.Lock()  # 创建锁

# 定义每个线程需要完成的工作
def worker(seed):
    for seed in seeds:
        # 做一些不需要锁的操作
        # 操作共享资源
        if mutex_w.acquire(1):  # 尝试获取锁
            thread_name = threading.current_thread().name  # 获取当前进程名
            print("%s starts writing the file" % thread_name)
            # 操作共享资源
            print("%s finishes writing the file" % thread_name)
            mutex_w.release()  # 释放锁


if __name__ == "__main__":
    # 本例中有15个线程，需要计算100次，尽可能平均得把计算任务分配给所有线程
    num_proc = 2  # 定义线程数
    seeds = [np.arange(i, 2, num_proc) for i in range(num_proc)]  # 把seed分给不同的线程进行处理

    thread_list = list()
    for i in range(num_proc):
        t = threading.Thread(target=worker, args=(seeds[i],))
        thread_list.append(t)

    # 启动所有线程
    for t in thread_list:
        t.start()