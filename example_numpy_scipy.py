import numpy
import scipy
from time import perf_counter

size = 1000000
print("----")

start_time = perf_counter()

scipy.stats.norm.rvs(loc=0.5, size=size)

end_time = perf_counter()
print("scipy.stats.norm.rvs(loc=0.5, size=size) - ", round(end_time-start_time, 4))
print("----")


start_time = perf_counter()

numpy_bin = numpy.random.normal(loc=0.5, size=size)

end_time = perf_counter()
print("numpy.random.normal(loc=0.5, size=size) - ", round(end_time-start_time, 4))
print("----")


start_time = perf_counter()

numpy_random_default_rng = numpy.random.default_rng(seed = numpy.random.Generator(numpy.random.PCG64()))
numpy_bin = numpy_random_default_rng.normal(loc=0.5, size=size)

end_time = perf_counter()
print("numpy_random_default_rng.normal(loc=0.5, size=size) - ", round(end_time-start_time, 4))
print("----")