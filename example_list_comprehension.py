from time import perf_counter

# List comprehension can have varying performance impact,
# depending on the complexity of the operation and object

print("----")

size = 10000000
# Using append within a loop
start_time = perf_counter()
numbers2 = []
for i in range(size):
    if i % 10 == 0:
        numbers2.append({"number":i, "multiple_of_10":True})
    else:
        numbers2.append({"number":i, "multiple_of_10":False})
end_time = perf_counter()
print("Building a list with append in a loop:    ", round(end_time-start_time, 2))
print("----")


# Using direct assignment in a loop
start_time = perf_counter()
numbers1 = [None] * size
for i in range(size):
    if i % 10 == 0:
        numbers1[i] = {"number":i, "multiple_of_10":True}
    else:
        numbers1[i] = {"number":i, "multiple_of_10":False}
end_time = perf_counter()
print("With direct assignment in a loop:         ", round(end_time-start_time, 2))
print("----")


# Building a list with list comprehension
start_time = perf_counter()
numbers = [{"number": x, "multiple_of_10":True} if x % 10 == 0 
           else {"number": x, "multiple_of_10":False}
           for x in range(size)]
end_time = perf_counter()
print("Building a list with list comprehension:  ", round(end_time-start_time, 2))
print("----")


# Filtering a list in a loop
start_time = perf_counter()
multiples_of_10 = []
for n in numbers:
    if n["multiple_of_10"]:
        multiples_of_10.append(n["number"])
end_time = perf_counter()
print("Filtering a list in a loop:               ", round(end_time-start_time, 2))
print("----")

# Filtering a list with list comprehension
start_time = perf_counter()
multiples_of_10_2 = [x["number"] for x in numbers if x["multiple_of_10"]]
end_time = perf_counter()
print("Filtering a list with list comprehension: ", round(end_time-start_time, 2))
print("----")

