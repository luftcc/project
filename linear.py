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


class Linear:
    num_keys = 0
    num_buckets = 0
    num_rehashing = 0
    step_size = 32
    alpha = 1
    table = []

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
                key = self.table[i][0]
                index = key % N
                while len(new_table[index]) != 0:
                    index = (index + 1) % N

                new_table[index] = [key]

        self.table = new_table
        self.num_buckets = N

    def load_factor(self):
        if (self.num_keys == 0):
            return 0
        if valid(self.num_buckets) and self.num_buckets != 0:
            return (self.num_keys + 1) / self.num_buckets
        else:
            return 0

    def search(self, key):
        if valid(key):
            index = key % self.num_buckets
            while len(self.table[index]) != 0:
                if self.table[index][0] == key:
                    return True, index
                else:
                    index = (index + 1) % self.num_buckets
            return False, index
        else:
            print("Invalid key to search: ", key)
            return False, -1

    def put(self, key):
        if valid(key):
            if self.load_factor() >= self.alpha:
                self.re_hashing();

            found, index = self.search(key)
            if not found:
                self.table[index] = [key]
                self.num_keys += 1
            else:
                pass
            return index

        else:
            print("Invalid key to put:", key)
            return -1

    def delete(self, key):
        if valid(key):
            found, index = self.search(key)
            if not found:
                return -1
            else:
                cur_index = index
                next_index = (cur_index + 1) % self.num_buckets
                while self.table[next_index] != []:
                    if not self.in_range(self.table[next_index][0], cur_index, next_index):
                        self.table[cur_index][0] = self.table[next_index][0]
                        cur_index = next_index
                    next_index = (next_index + 1) % self.num_buckets

                self.table[cur_index] = []

                self.num_keys -= 1
        else:
            print("Invalid key to delete:", key)
            return -1

    def in_range(self, key, i, j):
        index = key % self.num_buckets
        if j < i:
            if ((i != self.num_buckets - 1 and (index >= i + 1 or index <= j)) or (
                    i == self.num_buckets - 1 and index <= j)):
                return True
            else:
                return False
        else:
            if (index >= i + 1 and index <= j):
                return True
            else:
                return False

    def collision(self):
        count = 0
        for i in range(len(self.table)):
            if (len(self.table[i]) != 0):
                key = self.table[i][0]
                if key % self.num_buckets != i:
                    count += 1

        return count


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
    lin = Linear()
    for i in test:
        lin.put(i)
    print("Linear Probing:")
    print("Running time:", time.process_time() - t0)
    print("# of buckets:", lin.num_buckets, "# of keys:", lin.num_keys, "load factor:", lin.load_factor(),
          "# of re-hashing:", lin.num_rehashing, "collisions:", lin.collision())

# 2. Change α
print("\n\nChange α")
test = []
alphas = [0.3, 0.5, 0.6, 0.8, 1]
for i in range(10000):
    test.append(math.floor(random.random() * 0x7FFFFFFF))

for j, alpha in enumerate(alphas):
    print("alpha: ", alphas[j])

    t0 = time.process_time()
    lin = Linear()
    lin.alpha = alpha
    for i in test:
        lin.put(i)
    print("Linear Probing:")
    print("Running time:", time.process_time() - t0)
    print("# of buckets:", lin.num_buckets, "# of keys:", lin.num_keys, "load factor:", lin.load_factor(),
          "# of re-hashing:", lin.num_rehashing, "collisions:", lin.collision())

# 3.Search Query
print("\n\nSearch Query:")

nums = [100, 500, 1000, 5000, 20000]
test = []
for i in range(20000):
    test.append(math.floor(random.uniform(0, 0x7FFFFFFF)))

lin = Linear()


for i in test:
    lin.put(i)

for j, num in enumerate(nums):
    print("# of searching keys:", num)

    print("Linear Probing:")
    t0 = time.process_time()
    for i in range(num):
        lin.search(test[i])
    print("Running time:", time.process_time() - t0)
