import numpy

evt_granny = {"type": "granny", "name": "granny"}
evt_miss = {"type": "miss", "name":"miss"}

evt_receipt = {"type":"receipt", "name":"receipt"}
evt_milk = {"type":"item", "name": "milk"}
evt_eggs = {"type":"item", "name": "eggs"}
evt_butter = {"type":"item", "name": "butter"}
evt_bread = {"type":"item", "name": "bread"}
evt_yoghurt = {"type":"item", "name": "yoghurt"}
evt_apples = {"type":"item", "name": "apples"}
evt_oranges = {"type":"item", "name": "oranges"}
evt_tinned_jackfruit = {"type":"item", "name": "tinned jackfruit"}
evt_noodles = {"type":"item", "name": "noodles"}
evt_mirin = {"type":"item", "name": "mirin"}
evt_jasmine_rice = {"type":"item", "name": "jasmine rice"}
evt_black_rice = {"type":"item", "name": "black rice"}
evt_chicken = {"type":"item", "name": "chicken"}
evt_cola = {"type":"item", "name": "cola"}
evt_prawns = {"type":"item", "name": "prawns"}

class Model:
    def __init__(self, logger):
        self.logger = logger

    def run(self, inputs, seed, iterations):
        self.logger.info("Running simulation")

        # Store inputs for reference later
        item_inputs = inputs.pop("items")
        core_inputs = inputs
        core_inputs["num_items"] = len(item_inputs)

        # Use a predetermined seed so that we can have deterministic simulations
        random_state = numpy.random.Generator(
            numpy.random.PCG64(seed))
        numpy_gen = numpy.random.default_rng(seed=random_state)

        # Pick a random point on a normal curve for the average item time
        avg_rate = core_inputs["shop_time_mins"] / (core_inputs["num_items"] * (1 + core_inputs["blocked_by_granny_prob"]))
        item_minutes_rate = numpy_gen.normal(loc=avg_rate, scale=avg_rate/10)
        minimum_item_time = item_minutes_rate*0.1

        # Precalculate the numpy operations in bulk
        rand_item_times, rand_items_found, rand_items_reached, rand_granny_blocks = self.precalculate(numpy_gen, iterations, core_inputs, item_inputs, item_minutes_rate)

        # Now run our simulation
        result = []
        for i in range(iterations):
            result.append(self.iterate(iterations, i, item_inputs, minimum_item_time, rand_item_times, rand_items_found, rand_items_reached, rand_granny_blocks))

        # Our result is a simulation of the whole shopping trip
        return result


    def precalculate(self, rng, iterations, core_inputs, item_inputs, item_minutes_rate):
        # We will be estimating time for each item, in each iteration
        num_items = core_inputs["num_items"]
        num_item_sims = iterations * num_items

        # We will need that many granny block picks
        rand_granny_blocks = rng.binomial(n=1, p=core_inputs["blocked_by_granny_prob"], size=num_item_sims)

        # We need to pick a time for each item, each iteration, and it's cheaper to just 
        # double it here for granny blocks than to count the number that we need from previous results
        size = num_item_sims * 2
        rand_item_times = rng.normal(loc=item_minutes_rate, scale=item_minutes_rate/2, size=size)

        # Generate the found/reached binomial picks for each item
        item_find_probs = []
        item_reach_probs = []
        for i in item_inputs:
            item_find_probs.append(i["find_prob"])
            item_reach_probs.append(i["reach_prob"])

        # These produce a list of lists - each inner list has one pick for each item probability
        rand_items_found = rng.binomial(n=1, p=item_find_probs, size=[iterations, num_items])
        rand_items_reached = rng.binomial(n=1, p=item_reach_probs, size=[iterations, num_items])

        return rand_item_times, rand_items_found, rand_items_reached, rand_granny_blocks


    def iterate(self, iterations, iter_idx, item_inputs, minimum_item_time, rand_item_times, rand_items_found, rand_items_reached, rand_granny_blocks):
        logger = self.logger
        result = []

        # Simulate each item on the list
        item_idx = 0 # the index of this item in the found/reached lists
        for item in item_inputs:
            global_item_idx = iter_idx * item_idx
            global_item_idx_time = global_item_idx * 2
            actions = self.process_item(item, minimum_item_time, rand_item_times[global_item_idx_time:global_item_idx_time+2], rand_items_found[iter_idx][item_idx], rand_items_reached[iter_idx][item_idx], rand_granny_blocks[global_item_idx])
            result.extend(actions)
            item_idx += 1

        # Add the receipt action
        receipt = self.build_receipt(result)
        result.append(receipt)

        if iter_idx % 10000 == 0:
            logger.info("%d of %d complete...", iter_idx, iterations)

        # Return our result
        return result


    def process_item(self, item, minimum_item_time, rand_item_times, found, reached, blocked):
        actions = []

        # Calculate the time spent looking for the item
        find_time = rand_item_times[0]
        # Minimum item time of 10% item rate
        if find_time < minimum_item_time:
            find_time = minimum_item_time

        # Did I find the item?
        # If I've found the item, can I reach it?
        item_bagged = found and reached

        # Check for a last second granny block
        if blocked:
            # Calculate the time I was waiting 
            block_time = rand_item_times[1]
            if block_time < minimum_item_time:
                block_time = minimum_item_time

            # Add the block to the action list
            actions.append({"action": evt_granny, "time":block_time})
        
        if item_bagged:
            # Pick the right object for the item
            match item["name"]:
                case "milk":
                    item = evt_milk
                case "eggs":
                    item = evt_milk
                case "butter":
                    item = evt_butter
                case "bread":
                    item = evt_bread
                case "yoghurt":
                    item = evt_yoghurt
                case "apples":
                    item = evt_apples
                case "oranges":
                    item = evt_oranges
                case "tinned jackfruit":
                    item = evt_tinned_jackfruit
                case "noodles":
                    item = evt_noodles
                case "mirin":
                    item = evt_mirin
                case "jasmine rice":
                    item = evt_jasmine_rice
                case "black rice":
                    item = evt_black_rice
                case "chicken":
                    item = evt_chicken
                case "cola":
                    item = evt_cola
                case "prawns":
                    item = evt_prawns
                case _:
                    item = {"type":"item", "name": item["name"]}

            # Add the item action to our simulated shop
            actions.append({"action": item, "time":find_time})
        else:
            # Otherwise add a miss action with our wasted time
            actions.append({"action": evt_miss, "time":find_time})

        return actions


    def build_receipt(self, actions):
        receipt_items = []
        num_items = 0
        total_time = 0
        for a in actions:
            total_time += a["time"]
            if a["action"]["type"] == "item":
                receipt_items.append(a["action"]["name"])
                num_items += 1


        receipt = ", ".join(receipt_items)

        return {"action": evt_receipt, "items": receipt, "num_items":num_items, "time":total_time}
