import numpy

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
        self.item_minutes_rate = self.numpy_gen.normal(loc=avg_rate, scale=avg_rate/10, size=1)

        # Now run our simulation 
        result = []
        for i in range(iterations):
            result.append(self.iterate(i))

        # Our result is a simulation of the whole shopping trip
        return result


    def iterate(self, iter_idx):
        result = []

        # Simulate each item on the list
        for item in self.item_inputs:
            actions = self.process_item(item)
            for a in actions:
                result.append(a)

        # Add the receipt action
        receipt = self.build_receipt(result)
        result.append(receipt)

        if iter_idx % 10000 == 0:
            self.logger.info("%d of %d complete...", iter_idx, self.iterations)

        # Return our result
        return result


    def process_item(self, item):
        actions = []

        # Calculate the time spent looking for the item
        find_time = self.numpy_gen.normal(loc=self.item_minutes_rate, scale=self.item_minutes_rate/2)
        # Minimum item time of 10% item rate
        find_time = max(find_time, self.item_minutes_rate*0.1)

        item_bagged = False
        # Did I find the item?
        found = self.numpy_gen.binomial(n=1, p=item["find_prob"], size=1)
        if found:
            # I've found the item, now can I reach it?
            reached = self.numpy_gen.binomial(n=1, p=item["reach_prob"], size=1)
            if reached:
                item_bagged = True

        # Check for a last second granny block
        blocked = self.numpy_gen.binomial(n=1, p=self.core_inputs["blocked_by_granny_prob"], size=1)
        if blocked:
            # Calculate the time I was waiting 
            block_time = self.numpy_gen.normal(loc=self.item_minutes_rate, scale=self.item_minutes_rate/2)
            block_time = max(block_time, self.item_minutes_rate*0.1) # Minimum block time of 10% item rate
            # Add the block to the action list
            actions.append({"action": {"type":"granny", "name":"granny"}, "time":block_time})
        
        if item_bagged:
            # Add the item action to our simulated shop
            actions.append({"action": {"type":"item", "name":item["name"]}, "time":find_time})
        else:
            # Otherwise add a miss action with our wasted time
            actions.append({"action": {"type":"miss", "name":"miss"}, "time":find_time})

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

        return {"action": {"type:":"receipt", "name":"receipt"}, "items": receipt, "num_items":len(receipt_items), "time":total_time}
