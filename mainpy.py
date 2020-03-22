"""
    Program executable file
"""
import time
import threading
import settings
from db_work import DBWork
from generators import LetterGenerator
from request_work import Query


class Mythread(threading.Thread):

    def __init__(self, combinations, lock, storage):
        self.combinations = combinations
        self.storage = storage
        self.query_work = Query(settings.URL_TARGET)
        self.thread_lock = lock
        threading.Thread.__init__(self)

    def run(self):
        self.single_query(self.combinations)

    def single_query(self, combinations):
        result = self.query_work.do_query_post(combinations)
        with self.thread_lock:
            self.storage.insert_last_combinations(combinations)
            self.storage.inser_data_sucsseful(combinations, result['querys'], result['products'], result['categories'],
                                              result['status'], result['message'])


if __name__ == "__main__":
   storages = DBWork()
   th_locks = []
   locks = threading.Lock()
   generate = LetterGenerator(settings.ALPHABET)
   generate.start_generate()
   generator_list = generate.det_result_list()
   """
       Check if the code was interrupted at runtime
   """
   last_cmd = storages.get_last_combinations()
   if last_cmd[0] != 'empty':
       index = generator_list.index(last_cmd[0])
       work_generate = generator_list[index:]
   else:
       work_generate = generator_list

   for combination in work_generate:
       th = Mythread(combination, locks, storages)
       th.start()
       th_locks.append(th)
       time.sleep(1)

   for th_single in th_locks:
       th_single.join()
   storages.insert_last_combinations('empty')