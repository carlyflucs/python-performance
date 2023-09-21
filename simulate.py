import logging
from sys import stderr, argv
from time import perf_counter

from models.v0_base import Model as Model_v0
from models.v1_numpy import Model as Model_v1
from models.v2_runtime import Model as Model_v2
from models.v3_types import Model as Model_v3
from models.v4_interning import Model as Model_v4
from models.v5_final import Model as Model_v5
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
        case "v0":
            model = Model_v0(logger)
        case "v1":
            model = Model_v1(logger)
        case "v2":
            model = Model_v2(logger)
        case "v3":
            model = Model_v3(logger)
        case "v4":
            model = Model_v4(logger)
        case "v5":
            model = Model_v5(logger)
        case "v6":
            model = Model_v6(logger)

    # Start the simulation
    start_sim = perf_counter()

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

    results = model.run(inputs, seed, iterations)

    end_sim = perf_counter()
    sim_time = end_sim - start_sim
    sims_per_second = iterations / sim_time
    logger.info(
            f" |    |--> Performance: {sim_time:0.4f} seconds. ({sims_per_second:0.4f} iterations/sec)")

    # for i in results:
    #     print("[")
    #     print(*i, sep='\n  ')
    #     print("]")