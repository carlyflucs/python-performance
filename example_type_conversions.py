import numpy.random as rand
from time import perf_counter


print("----")
binom_no_size = rand.binomial(n=1, p=0.5)
print("rand.binomial(n=1, p=0.5):", type(binom_no_size), binom_no_size)

print("----")
binom_size = rand.binomial(n=1, p=0.5, size=1)
print("rand.binomial(n=1, p=0.5, size=1):", type(binom_size), binom_size)

print("----")


size = 10000000 # 10 million

# Calculating max of two integers
start_time = perf_counter()
for i in range(size):
    x = max(i, binom_no_size)
end_time = perf_counter()
print("Calculating max of two integers:                    ", round(end_time-start_time, 2))
print("----")


# Calculating max of integer and single item ndarray
start_time = perf_counter()
for i in range(size):
    x = max(i, binom_size)
end_time = perf_counter()
print("Calculating max of integer and single item ndarray: ", round(end_time-start_time, 2))
print("----")