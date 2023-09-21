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
        self.iterations = iterations

        # Store inputs for reference later
        self.item_inputs = inputs.pop("items")
        self.core_inputs = inputs
        self.core_inputs["num_items"] = len(self.item_inputs)

        # Use a predetermined seed so that we can have deterministic simulations
        self.random_state = numpy.random.Generator(
            numpy.random.PCG64(seed))
        self.numpy_gen = numpy.random.default_rng(seed=self.random_state)

        # Pick a random point on a normal curve for the average item time
        avg_rate = self.core_inputs["shop_time_mins"] / (self.core_inputs["num_items"] * (1 + self.core_inputs["blocked_by_granny_prob"]))
        self.item_minutes_rate = self.numpy_gen.normal(loc=avg_rate, scale=avg_rate/10)

        # Precalculate the numpy operations in bulk
        self.precalculate(iterations)

        # Now run our simulation
        result = []
        for i in range(iterations):
            result.append(self.iterate(i))

        # Our result is a simulation of the whole shopping trip
        return result


    def precalculate(self, iterations):
        # We will be estimating time for each item, in each iteration
        num_items = self.core_inputs["num_items"]
        num_item_sims = iterations * num_items
        rng = self.numpy_gen

        # We will need that many granny block picks
        self.rand_granny_blocks = rng.binomial(n=1, p=self.core_inputs["blocked_by_granny_prob"], size=num_item_sims)

        # We need to pick a time for each item, each iteration, and it's cheaper to just 
        # double it here for granny blocks than to count the number that we need from previous results
        size = num_item_sims * 2
        self.rand_item_times = rng.normal(loc=self.item_minutes_rate, scale=self.item_minutes_rate/2, size=size)

        # Generate the found/reached binomial picks for each item
        item_find_probs = []
        item_reach_probs = []
        for i in self.item_inputs:
            item_find_probs.append(i["find_prob"])
            item_reach_probs.append(i["reach_prob"])

        # These produce a list of lists - each inner list has one pick for each item probability
        self.rand_items_found = rng.binomial(n=1, p=item_find_probs, size=[iterations, num_items])
        self.rand_items_reached = rng.binomial(n=1, p=item_reach_probs, size=[iterations, num_items])


    def iterate(self, iter_idx):
        result = []

        # Simulate each item on the list
        item_idx = 0 # the index of this item in the found/reached lists
        for item in self.item_inputs:
            actions = self.process_item(item, iter_idx, item_idx)
            for a in actions:
                result.append(a)
            item_idx += 1

        # Add the receipt action
        receipt = self.build_receipt(result)
        result.append(receipt)

        if iter_idx % 10000 == 0:
            self.logger.info("%d of %d complete...", iter_idx, self.iterations)

        # Return our result
        return result


    def process_item(self, item, iter_idx, item_idx):
        actions = []

        # There are 2 item times allocated for each item
        item_time_idx = iter_idx * item_idx * 2

        # Calculate the time spent looking for the item
        find_time = self.rand_item_times[item_time_idx]
        # Minimum item time of 10% item rate
        find_time = max(find_time, self.item_minutes_rate*0.1)

        item_bagged = False
        # Did I find the item?
        found = self.rand_items_found[iter_idx][item_idx]
        if found:
            # I've found the item, now can I reach it?
            reached = self.rand_items_reached[iter_idx][item_idx]
            if reached:
                item_bagged = True

        # Check for a last second granny block
        blocked = self.rand_granny_blocks[iter_idx * item_idx]
        if blocked:
            # Calculate the time I was waiting 
            block_time = self.rand_item_times[item_time_idx + 1]
            block_time = max(block_time, self.item_minutes_rate*0.1) # Minimum block time of 10% item rate
            # Add the block to the action list
            actions.append({"action": evt_granny, "time":block_time})
        
        if item_bagged:
            # Pick the right object for the item
            match item["name"]:
                case "milk":
                    item = evt_milk
                case "eggs":
                    item = evt_eggs
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
        total_time = 0
        for i in range(len(actions)):
            total_time += actions[i]["time"]

            if actions[i]["action"]["type"] == "item":
                receipt_items.append(actions[i]["action"]["name"])
        
        receipt = ""
        for i in range(len(receipt_items)):
            receipt = receipt + receipt_items[i]
            if i < len(receipt_items) - 1:
                receipt = receipt + ", "

        return {"action": evt_receipt, "items": receipt, "num_items":len(receipt_items), "time":total_time}
