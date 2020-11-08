# TODO: In progress but moving code out of the way

class LogIter:
    def __init__(self):
        self.count = 0
        self.iteration = 1
        self.bigger_iteration = 10

    def iter(self):
        self.count += 1
        if not self.count % self.iteration:
            print("Iter: %d" % self.count)
        if not self.count  % self.bigger_iteration:
            self.iteration = self.bigger_iteration
            self.bigger_iteration *= 10


def breed(all_clones, generation):
    clones = list(all_clones.clones())
    num_clones = len(clones)
    logger = LogIter()

    for i in range(num_clones):
        for j in range(i, num_clones):
            for k in range(j, num_clones):
                clone1 = clones[i]
                clone2 = clones[j]
                clone3 = clones[k]
                box = Box([clone1, clone2, clone3], generation)
                result = box.get_offspring()
                all_clones.add_clone(result)
                logger.iter()

    for i in range(num_clones):
        for j in range(i, num_clones):
            for k in range(j, num_clones):
                for l in range(k, num_clones):
                    clone1 = clones[i]
                    clone2 = clones[j]
                    clone3 = clones[k]
                    clone4 = clones[l]
                    box = Box([clone1, clone2, clone3, clone4], generation)
                    result = box.get_offspring()
                    all_clones.add_clone(result)
                    logger.iter()


def check_targets(all_clones, targets):
    completed_targets = []
    for target_clone in targets:
        completed_target = all_clones.get_equivalent(target_clone)
        if completed_target != None:
