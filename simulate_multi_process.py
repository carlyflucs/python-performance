import logging
from multiprocessing import Process, Queue, cpu_count
from sys import stderr, argv
from time import perf_counter

from models.v6_multi import Model as Model_v6

if __name__ == "__main__":
    # Set up logger so our logs don't get captured in std out
    logger = logging.getLogger()
    handler = logging.StreamHandler(stderr)
    logger.addHandler(handler)
    logger.setLevel("INFO")

    # Check inputs so we know which model is being run
    ver = ""
    if len(argv) > 1:
        ver = argv[1]
            
    # Initialise the model
    match ver:
        case _:
            model = Model_v6(logger)

    iterations = 100000
    seed = 1234
    inputs = {
        "shop_time_mins": 22.5,
        "blocked_by_granny_prob": 0.20,
        "items": [
            {"name": "milk", "reach_prob": 0.95, "find_prob":0.95},
            {"name": "eggs", "reach_prob": 0.9, "find_prob":0.8},
            {"name": "butter", "reach_prob": 0.75, "find_prob":0.99},
            {"name": "bread", "reach_prob": 0.85, "find_prob":0.75},
            {"name": "yoghurt", "reach_prob": 0.9, "find_prob":0.8},
            {"name": "apples", "reach_prob": 0.100, "find_prob":0.9},
            {"name": "oranges", "reach_prob": 0.100, "find_prob":0.85},
            {"name": "tinned jackfruit", "reach_prob": 0.8, "find_prob":0.15},
            {"name": "noodles", "reach_prob": 0.7, "find_prob":0.85},
            {"name": "mirin", "reach_prob": 0.9, "find_prob":0.75},
            {"name": "jasmine rice", "reach_prob": 0.95, "find_prob":0.95},
            {"name": "black rice", "reach_prob": 0.5, "find_prob":0.25},
            {"name": "chicken", "reach_prob": 0.95, "find_prob":0.8},
            {"name": "cola", "reach_prob": 0.9, "find_prob":0.1},
            {"name": "prawns", "reach_prob": 1.0, "find_prob":0.3},
        ]
    }

    start_sim = perf_counter()
    
    q = Queue()
    process_count = cpu_count()
    process_iterations = int(iterations/process_count)
    processes = []
    all_results = []
    for i in range(process_count):
        p = Process(target=model.run, args=(inputs, seed, process_iterations, q))
        processes.append(p)
        seed += 1

    for p in processes:
        p.start()
    for p in processes:
        ret = q.get() # receive result
        print("Received result", p)
    for p in processes:
        p.close()

    end_sim = perf_counter()
    sim_time = end_sim - start_sim
    sims_per_second = iterations / sim_time
    logger.info(
            f" |    |--> Performance: {sim_time:0.4f} seconds. ({sims_per_second:0.4f} iterations/sec)")

    # for i in all_results:
    #     print("[")
    #     print(*i, sep='\n  ')
    #     print("]")