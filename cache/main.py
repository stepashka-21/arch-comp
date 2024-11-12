import sys
M, N, K = 64, 60, 32


class Cache:
    def __init__(self, MEM_SIZE, ADDR_LEN, CACHE_WAY, CACHE_TAG_LEN, CACHE_IDX_LEN, CACHE_OFFSET_LEN, CACHE_SIZE,
                 CACHE_LINE_SIZE, CACHE_LINE_COUNT, CACHE_SETS_COUNT, policy):

        self.MEM_SIZE = MEM_SIZE
        self.ADDR_LEN = ADDR_LEN
        self.CACHE_WAY = CACHE_WAY
        self.CACHE_TAG_LEN = CACHE_TAG_LEN
        self.CACHE_IDX_LEN = CACHE_IDX_LEN
        self.CACHE_OFFSET_LEN = CACHE_OFFSET_LEN
        self.CACHE_SIZE = CACHE_SIZE
        self.CACHE_LINE_SIZE = CACHE_LINE_SIZE
        self.CACHE_LINE_COUNT = CACHE_LINE_COUNT
        self.CACHE_SETS_COUNT = CACHE_SETS_COUNT
        self.policy = policy  # политика вытеснения кэша
        self.cache = [[-1] * self.CACHE_WAY for _ in range(CACHE_SETS_COUNT)]
        self.time_for_all = [[0] * self.CACHE_WAY for _ in range(CACHE_SETS_COUNT)]
        self.cache_hit = 6  # время, через которое в результате кэш попадания, кэш начинает отвечать
        self.cache_miss = 4  # время, через которое в результате кэш промаха, кэш посылает запрос к памяти
        self.mem_answer = 100  # время, через которое память начинает отвечать
        self.A = 1  # "по шинам A1 и A2 адрес передаётся за 1 такт"
        self.C = 1  # "по шинам C1 и C2 команда передаётся за 1 такт"
        self.D = 16  # отправка данных
        self.add = 1  # сложение
        self.init = 1  # инициализация переменных
        self.loop = 1  # переход на новую итерацию цикла
        self.exit = 1  # выход из функции занимают
        self.mul = 5  # умножение
        self.mem = 1  # обращение к памяти вида pc[x]
        self.wr = 0  # количество записей (не перезаписей), их столько же, сколько всего мест, 64, но пусть будет
        self.k = 0  # количество перезаписей pc[x]=s

    def read(self, ind_i, tag, policy):
        ind_j = -1
        if policy == "lru":
            for j in range(self.CACHE_WAY):
                if self.cache[ind_i][j] == tag:
                    ind_j = j
                    break
            if ind_j != -1:
                for j in range(self.CACHE_WAY):
                    if self.time_for_all[ind_i][j] > 0:
                        self.time_for_all[ind_i][j] += 1
        else:
            for j in range(self.CACHE_WAY):
                if self.cache[ind_i][j] == tag:
                    ind_j = j
                    break
            if sum(self.time_for_all[ind_i]) == 3 and self.time_for_all[ind_i][ind_j] == 0 and ind_j != -1:
                for j in range(self.CACHE_WAY):
                    if self.time_for_all[ind_i][j] == 1:
                        self.time_for_all[ind_i][j] = 0
                    else:
                        self.time_for_all[ind_i][j] = 1

        return ind_j

    def old_lru(self, ind_i):
        ind_j = -1
        old = 0
        for j in range(self.CACHE_WAY):
            if self.time_for_all[ind_i][j] > old:
                old = self.time_for_all[ind_i][j]
                ind_j = j
            elif self.time_for_all[ind_i][j] == 0:
                ind_j = j
                self.wr += 1  # просто запись
                break
        for j in range(self.CACHE_WAY):
            if self.time_for_all[ind_i][j] > 0:
                self.time_for_all[ind_i][j] += 1
        return ind_j

    def old_plru(self, ind_i):
        ind_j = -1
        s = sum(self.time_for_all[ind_i])
        if s == 3:
            for j in range(self.CACHE_WAY):
                if self.time_for_all[ind_i][j] == 1:
                    self.time_for_all[ind_i][j] = 0
                else:
                    self.time_for_all[ind_i][j] = 1
                    ind_j = j
        else:
            for j in range(self.CACHE_WAY):
                if self.time_for_all[ind_i][j] == 0:
                    self.time_for_all[ind_i][j] = 1
                    ind_j = j
                    break
        if self.cache[ind_i][ind_j] == -1:
            self.wr += 1  # просто запись
        return ind_j

    def write(self, ind_i, ind_j, tag):
        self.cache[ind_i][ind_j] = tag


def mmul(policy):
    a = [[0] * K for _ in range(M)]
    b = [[0] * N for _ in range(K)]
    c = [[0] * N for _ in range(M)]
    # получаем адреса каждой клетки матриц
    data = 0
    for i in range(M):
        for j in range(K):
            a[i][j] = data
            data += 1
    for i in range(K):
        for j in range(N):
            b[i][j] = data
            data += 2
    for i in range(M):
        for j in range(N):
            c[i][j] = data
            data += 4

    cache = Cache(MEM_SIZE=512 * 1024,
                  ADDR_LEN=19,
                  CACHE_WAY=4,
                  CACHE_TAG_LEN=10,
                  CACHE_IDX_LEN=4,
                  CACHE_OFFSET_LEN=5,
                  CACHE_SIZE=2048,
                  CACHE_LINE_SIZE=32,
                  CACHE_LINE_COUNT=64,
                  CACHE_SETS_COUNT=16, policy=policy)

    def get_addr(x):
        return (x >> cache.CACHE_OFFSET_LEN) % cache.CACHE_SETS_COUNT, x >> (cache.CACHE_OFFSET_LEN
                                                                             + cache.CACHE_IDX_LEN)
    total_time = 0
    miss = 0
    query = 0

    total_time += cache.init * 2

    for y in range(M):

        total_time += cache.loop + cache.add
        total_time += cache.add * 2

        for x in range(N):

            total_time += cache.loop + cache.add
            total_time += cache.init * 3

            for k in range(K):

                total_time += cache.loop + cache.add
                total_time += cache.add
                total_time += cache.mul + cache.add

                ind_a, tag_a = get_addr(a[y][k])
                ind_a, tag_a = int(ind_a), int(tag_a)
                total_time += cache.A
                ja = cache.read(ind_a, tag_a, policy)
                query += 1

                if policy == "lru":
                    if ja == -1:  # запись
                        ja = cache.old_lru(ind_a)
                        cache.write(ind_a, ja, tag_a)

                        miss += 1
                        total_time += cache.mem_answer + cache.cache_miss + cache.D + cache.mem

                    else:  # чтение
                        total_time += cache.cache_hit
                    cache.time_for_all[ind_a][ja] = 1

                else:
                    if ja == -1:  # запись
                        ja = cache.old_plru(ind_a)
                        cache.write(ind_a, ja, tag_a)

                        miss += 1
                        total_time += cache.mem_answer + cache.cache_miss + cache.D + cache.mem

                    else:  # чтение
                        total_time += cache.cache_hit
                    cache.time_for_all[ind_a][ja] = 1

                ind_b, tag_b = get_addr(b[k][x])
                ind_b, tag_b = int(ind_b), int(tag_b)
                total_time += cache.A
                jb = cache.read(ind_b, tag_b, policy)
                query += 1

                if policy == "lru":
                    if jb == -1:  # запись
                        jb = cache.old_lru(ind_b)
                        cache.write(ind_b, jb, tag_b)

                        miss += 1
                        total_time += cache.mem_answer + cache.cache_miss + cache.D + cache.mem

                    else:  # чтение
                        total_time += cache.cache_hit
                    cache.time_for_all[ind_b][jb] = 1
                else:
                    if jb == -1:  # запись
                        jb = cache.old_plru(ind_b)
                        cache.write(ind_b, jb, tag_b)

                        miss += 1
                        total_time += cache.mem_answer + cache.cache_miss + cache.D + cache.mem

                    else:  # чтение
                        total_time += cache.cache_hit
                    cache.time_for_all[ind_b][jb] = 1

            ind_c, tag_c = get_addr(c[y][x])
            ind_c, tag_c = int(ind_c), int(tag_c)
            total_time += 2 * cache.A
            jc = cache.read(ind_c, tag_c, policy)
            query += 1

            if policy == "lru":
                if jc == -1:  # запись
                    before = cache.wr
                    jc = cache.old_lru(ind_c)
                    cache.write(ind_c, jc, tag_c)
                    after = cache.wr

                    miss += 1
                    total_time += cache.mem_answer + cache.cache_miss + cache.D + cache.mem

                    if before == after:  # изменилось ли число просто-записей
                        total_time += cache.D + cache.mem_answer + cache.mem
                        cache.k += 1

                else:  # чтение
                    total_time += cache.cache_hit
                    for j in range(cache.CACHE_WAY):
                        if cache.time_for_all[ind_c][j] != 0:
                            cache.time_for_all[ind_c][j] += 1
                cache.time_for_all[ind_c][jc] = 1
            else:
                if jc == -1:  # запись
                    before = cache.wr
                    jc = cache.old_plru(ind_c)
                    cache.write(ind_c, jc, tag_c)
                    after = cache.wr

                    miss += 1
                    total_time += cache.mem_answer + cache.cache_miss + cache.D + cache.mem

                    if before == after:  # изменилось ли число просто-записей
                        total_time += cache.D + cache.mem_answer + cache.mem
                        cache.k += 1

                else:  # чтение
                    total_time += cache.cache_hit
                cache.time_for_all[ind_c][jc] = 1

    total_time += cache.exit
    factor = 100 * (1 - miss / query)

    return factor, total_time


if __name__ == "__main__":
    s1 = mmul("lru")
    s2 = mmul("p-lru")

    def printf(for_mat, *args):
        sys.stdout.write(for_mat % args)

    printf("LRU:\thit perc. %3.4f%%\ttime: %u\npLRU:\thit perc. %3.4f%%\ttime: %u\n", s1[0], s1[1], s2[0], s2[1])
