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


class Chained:
    num_keys = 0
    num_buckets = 0
    num_rehashing = 0
    step_size = 32
    alpha = 1
    table = [];

    def __init__(self):
        self.num_keys = 0
        self.num_buckets = 23
        self.num_rehashing = 0
        self.table = []
        self.alpha = 1
        for i in range(self.num_buckets):
            self.table.append([])

    def next_prime(self):
        N = self.num_buckets
        while (True):
            N += self.step_size
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
                    index = k % N
                    new_table[index].append(k)
        self.table = new_table
        self.num_buckets = N

    def collision(self):
        count = 0
        for i in range(len(self.table)):
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

    def search(self, key):
        if valid(key):
            index = key % self.num_buckets
            for i in range(len(self.table[index])):
                if key == self.table[index][i]:
                    return True, index, i
            return False, index, len(self.table[index])
        else:
            print("Invalid key to search: ", key)
            return False, -1, -1

    def put(self, key):
        if valid(key):
            if self.load_factor() >= self.alpha:
                self.re_hashing();

            found, index, chain_index = self.search(key)
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
    cha = Chained()
    for i in test:
        cha.put(i)
    print("Chained Hashing:")
    print("Running time:", time.process_time() - t0)
    print("# of buckets:", cha.num_buckets, "# of keys:", cha.num_keys, "load factor:", cha.load_factor(),
          "# of re-hashing:", cha.num_rehashing, "collisions:", cha.collision())



print("\n\nChange α")
test = []
alphas = [0.3, 0.5, 0.6, 0.8, 1]
for i in range(10000):
    test.append(math.floor(random.random() * 0x7FFFFFFF))

for j, alpha in enumerate(alphas):
    print("alpha: ", alphas[j])


    t0 = time.process_time()
    cha = Chained()
    cha.alpha = alpha
    for i in test:
        cha.put(i)
    print("Chained Hashing:")
    print("Running time:", time.process_time() - t0)
    print("# of buckets:", cha.num_buckets, "# of keys:", cha.num_keys, "load factor:", cha.load_factor(),
          "# of re-hashing:", cha.num_rehashing, "collisions:", cha.collision())

# 3.Search Query
print("\n\nSearch Query:")

nums = [100, 500, 1000, 5000, 20000]
test = []
for i in range(20000):
    test.append(math.floor(random.uniform(0, 0x7FFFFFFF)))


cha = Chained()


for i in test:
    cha.put(i)


for j, num in enumerate(nums):
    print("# of searching keys:", num)



    print("Chained Hashing:")
    t0 = time.process_time()
    for i in range(num):
        cha.search(test[i])
    print("Running time:", time.process_time() - t0)
