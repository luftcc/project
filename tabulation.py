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


class Tabulation:
    num_keys = 0
    num_buckets = 0
    num_rehashing = 0
    step_size = 32
    alpha = 1
    table = []
    t0 = []
    t1 = []
    t2 = []
    t3 = []

    def __init__(self):
        self.num_keys = 0
        self.num_buckets = 23
        self.num_rehashing = 0
        self.step_size = 32
        self.alpha = 1
        self.t0 = []
        self.t1 = []
        self.t2 = []
        self.t3 = []
        self.table = []

        for i in range(self.num_buckets):
            self.table.append([])

        for i in range(256):
            self.t0.append(math.floor(random.random() * 0xFFFFFFFF))
            self.t1.append(math.floor(random.random() * 0xFFFFFFFF))
            self.t2.append(math.floor(random.random() * 0xFFFFFFFF))
            self.t3.append(math.floor(random.random() * 0xFFFFFFFF))

    def next_prime(self):
        N = self.num_buckets
        while (True):
            N += self.step_size;
            if is_prime(N):
                return N

    def re_hashing(self):
        self.num_rehashing += 1
        N = self.next_prime()

        new_table = []
        for i in range(0, N):
            new_table.append([])

        for i in range(0, len(self.table)):
            if (len(self.table[i]) != 0):
                for k in self.table[i]:
                    index = self.hash_value(k) % N
                    new_table[index].append(k)

        # finally, set table reference to new_table, update num_buckets
        self.table = new_table
        self.num_buckets = N

    def collision(self):
        count = 0
        for i in range(0, len(self.table)):
            if (len(self.table[i]) != 0):
                count += 1

        return self.num_keys - count

    def load_factor(self):
        if (self.num_keys == 0):
            return 0
        if valid(self.num_buckets) and self.num_buckets != 0:
            return (self.num_keys + 1) / self.num_buckets
        else:
            return 0;

    def hash_value(self, key):
        k0 = key & 0xFF
        k1 = (key >> 8) & 0xFF
        k2 = (key >> 16) & 0xFF
        k3 = (key >> 24) & 0xFF
        T0 = self.t0[k0]
        T1 = self.t1[k1]
        T2 = self.t2[k2]
        T3 = self.t3[k3]
        res = T0 ^ T1 ^ T2 ^ T3
        return res

    def search(self, key):
        if valid(key):

            index = self.hash_value(key) % self.num_buckets
            # search the table(index) one by one
            for i in range(len(self.table[index])):
                if key == self.table[index][i]:
                    return True, index, i

            # out of for loop, not found
            return False, index, len(self.table[index])
        else:
            print("Invalid key to search: ", key)
            return False, -1, -1

    def put(self, key):
        if valid(key):
            # if adding this key will cause load_factor to be greater than or
            # equal to preset alpha, then first re-hashing, later on put(key)
            if self.load_factor() >= self.alpha:
                self.re_hashing();

            found, index, chain_index = self.search(key)
            # if found, nothing happens,
            # if not found, then append key to table[index] and increment num_keys
            # always return the inserted index
            if not found:
                self.table[index].append(key)
                self.num_keys += 1
            else:
                pass
            return index

        else:
            print("Invalid key to put:", key)
            return -1

    def delete(self, key):
        if valid(key):
            found, index, chain_index = self.search(key)

            # if found, set table[index] to be an empty list, decrement num_keys and return index
            # if not found, return -1
            if not found:
                return -1
            else:
                del self.table[index][chain_index]
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
    tab = Tabulation()
    for i in test:
        tab.put(i)
    print("Tabulation Hashing:")
    print("Running time:", time.process_time() - t0)
    print("# of buckets:", tab.num_buckets, "# of keys:", tab.num_keys, "load factor:", tab.load_factor(),
          "# of re-hashing:", tab.num_rehashing, "collisions:", tab.collision())


print("\n\nChange α")
test = []
alphas = [0.3, 0.5, 0.6, 0.8, 1]
for i in range(10000):
    test.append(math.floor(random.random() * 0x7FFFFFFF))

for j, alpha in enumerate(alphas):
    print("alpha: ", alphas[j])

    t0 = time.process_time()
    tab = Tabulation()
    tab.alpha = alpha
    for i in test:
        tab.put(i)
    print("Tabulation Hashing:")
    print("Running time:", time.process_time() - t0)
    print("# of buckets:", tab.num_buckets, "# of keys:", tab.num_keys, "load factor:", tab.load_factor(),
          "# of re-hashing:", tab.num_rehashing, "collisions:", tab.collision())

print("\n\nSearch Query:")

nums = [100, 500, 1000, 5000, 20000]
test = []
for i in range(20000):
    test.append(math.floor(random.uniform(0, 0x7FFFFFFF)))


tab = Tabulation()


for i in test:

    tab.put(i)


for j, num in enumerate(nums):
    print("# of searching keys:", num)




    print("Tabulation Hashing:")
    t0 = time.process_time()
    for i in range(num):
        tab.search(test[i])
    print("Running time:", time.process_time() - t0)
