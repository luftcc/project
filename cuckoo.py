import math
import random
import time


def valid(num):
    if type(num) == int and num >= 0:
        return True
    else:
        return False


def is_prime(num):
    if not valid(num):
        print("Invalid is_prime number: ", num)
        return False
    else:
        limit = math.floor(math.sqrt(num))
        for i in range(2, limit + 1):
            if (num % i == 0):
                return False
            else:
                pass

        return True


def next_prime(num):
    N = num
    while (True):
        N += 32;
        if is_prime(N):
            return N


class Cuckoo:
    num_keys = 0
    num_buckets = 0
    num_rehashing = 0
    step_size = 32
    alpha = 1
    table = [[], []]

    def __init__(self):
        self.num_keys = 0
        self.num_buckets = 23
        self.num_rehashing = 0
        self.alpha = 1
        self.table = [[], []]
        for i in range(self.num_buckets):
            self.table[0].append([])
            self.table[1].append([])

    def re_hashing(self):
        table0 = self.table[0]
        table1 = self.table[1]
        old_num_buckets = self.num_buckets
        old_num_rehashing = self.num_rehashing
        old_alpha = self.alpha
        step_size = self.step_size

        new_cuckoo = Cuckoo()
        new_cuckoo.step_size = step_size
        new_cuckoo.num_buckets = old_num_buckets
        new_cuckoo.num_buckets += step_size
        while is_prime(new_cuckoo.num_buckets) == False:
            new_cuckoo.num_buckets += step_size
        new_cuckoo.num_rehashing = old_num_rehashing + 1
        new_cuckoo.alpha = old_alpha
        new_cuckoo.num_keys = 0
        new_cuckoo.table = [[], []]
        for i in range(new_cuckoo.num_buckets):
            new_cuckoo.table[0].append([])
            new_cuckoo.table[1].append([])
        for i in range(len(table0)):
            if (len(table0[i]) != 0):
                new_cuckoo.put(table0[i][0])
            if (len(table1[i]) != 0):
                new_cuckoo.put(table1[i][0])
        self.num_buckets = new_cuckoo.num_buckets
        self.num_rehashing += 1
        self.table = new_cuckoo.table

    def load_factor(self):
        if (self.num_keys == 0):
            return 0
        if valid(self.num_buckets) and self.num_buckets != 0:
            return (self.num_keys + 1) / self.num_buckets
        else:
            return 0;

    def search(self, key):
        if valid(key):
            index0 = key % self.num_buckets
            index1 = math.floor((key / self.num_buckets)) % self.num_buckets
            key0 = self.table[0][index0]
            key1 = self.table[1][index1]
            if (key0 == [key]):
                return True, 0, index0
            if (key1 == [key]):
                return True, 1, index1
            else:
                if (key0 == []):
                    return False, 0, index0
                else:
                    return False, 1, index1
        else:
            print("Invalid key to search: ", key)
            return False, -1, -1

    def put(self, key):
        if valid(key):
            pass

            found, table, index = self.search(key)
            if found:
                return table, index
            else:
                pass
            if (len(self.table[table][index]) == 0):
                self.table[table][index] = [key]
                self.num_keys += 1
            else:
                cur_key = key
                cur_table = table
                cur_index = index

                while (True):
                    if (self.table[cur_table][cur_index] != []):
                        next_key = self.table[cur_table][cur_index][0]
                        next_table = 1 - cur_table
                        next_index = next_key % self.num_buckets if next_table == 0 else math.floor(
                            (next_key / self.num_buckets)) % self.num_buckets

                        self.table[cur_table][cur_index] = [cur_key]

                        cur_key = next_key
                        cur_table = next_table
                        cur_index = next_index
                    else:
                        self.table[cur_table][cur_index] = [cur_key]
                        self.num_keys += 1
                        return cur_table, cur_index
                    if (cur_key == key and cur_table == table):
                        self.re_hashing();
                        return self.put(cur_key)

        else:
            print("Invalid key to put:", key)
            return -1

    def delete(self, key):
        if valid(key):
            found, table, index = self.search(key)
            if not found:
                return -1
            else:
                self.table[table][index] = []
                self.num_keys -= 1
        else:
            print("Invalid key to delete:", key)
            return -1

print("\n\nChange number of keys inserted")
nums = [100, 500, 1000, 5000, 20000]
tests = []
for i, num in enumerate(nums):
    tests.append([])
    for j in range(num):
        tests[i].append(math.floor(random.uniform(0, 0x7FFFFFFF)))

for j, test in enumerate(tests):
    print("Number of keys inserted(containing duplicate): ", nums[j])



    t0 = time.process_time()
    cuc = Cuckoo()
    for i in test:
        cuc.put(i)
    print("Cuckoo Hashing:")
    print("Running time:", time.process_time() - t0)
    print("# of buckets:", cuc.num_buckets, "# of keys:", cuc.num_keys, "load factor:", cuc.load_factor(),
          "# of re-hashing:", cuc.num_rehashing)



print("\n\nSearch Query:")

nums = [100, 500, 1000, 5000, 20000]
test = []
for i in range(20000):
    test.append(math.floor(random.uniform(0, 0x7FFFFFFF)))

cuc = Cuckoo()

for i in test:
    cuc.put(i)

for j, num in enumerate(nums):
    print("# of searching keys:", num)

    print("Cuckoo Hashing:")
    t0 = time.process_time()
    for i in range(num):
        cuc.search(test[i])
    print("Running time:", time.process_time() - t0)