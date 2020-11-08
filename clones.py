import csv
from box import Box
from clone import Clone
from result import Result
from clonestorage import CloneStorage

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
            completed_targets.append(completed_target)
            targets.remove(target_clone)
    return completed_targets

def get_path_to_targets(targets, max_generation):
    generations = [set()] * max_generation
    while len(targets) > 0:
        new_targets = []
        for target in targets:
            target_box = target.get_box()
            generation = 0 if target_box is None else target_box.get_generation()
            if target in generations[generation]:
                continue
            generations[generation].add(target)
            if target_box is not None:
                new_targets.extend(target_box.get_parents())
        targets = new_targets
    return generations

def print_generations(generations):
    for i in range(len(generations)):
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("Generation: %d" % (i))
        clones = list(generations[i])
        for clone in clones:
            print(clone.get_result())

def find_specific(all_clones):
    targets = [Clone("YYYYYY"), Clone("GYYYYY"), Clone("GGYYYY"),
            Clone("GGGYYY"), Clone("GGGGYY"), Clone("GGGGGY"), Clone("GGGGGG")]
    completed_targets = []
    current_size = all_clones.size()
    generation_count = 0
    while True:
        generation_count += 1
        print("Generation: %d" % generation_count)
        breed(all_clones, generation_count)
        completed_targets.append(check_targets(all_clones, targets))
        if len(targets) == 0:
            print("Done")
            break
        new_size = all_clones.size()
        if new_size == current_size:
            print("Ran out of possible clones")
            break
        if generation_count == 20:
            print("Hit 20 generations")
            break
    generations = get_path_to_targets(completed_targets, max_generation)
    print_generations(generations)

def find_best(all_clones):
    clones = list(all_clones.clones())
    best_score = -100
    best_clones = set()
    num_clones = len(clones)
    for i in range(num_clones):
        for j in range(i, num_clones):
            for k in range(j, num_clones):
                for l in range(k, num_clones):
                    clone1 = clones[i]
                    clone2 = clones[j]
                    clone3 = clones[k]
                    clone4 = clones[l]
                    box = Box([clone1, clone2, clone3, clone4], 1)
                    result = box.get_offspring()
                    if result in all_clones.clones():
                        continue
                    score = result.score()
                    if score > best_score:
                        best_score = score
                        best_clones = set()
                    if score == best_score:
                        resultBox = Result(result, box)
                        best_clones.add(resultBox)

    for i in range(num_clones):
        for j in range(i, num_clones):
            for k in range(j, num_clones):
                clone1 = clones[i]
                clone2 = clones[j]
                clone3 = clones[k]
                box = Box([clone1, clone2, clone3], 1)
                result = box.get_offspring()
                if result in all_clones.clones():
                    continue
                score = result.score()
                if score > best_score:
                    best_score = score
                    best_clones = set()
                if score == best_score:
                    resultBox = Result(result, box)
                    best_clones.add(resultBox)
    sorted_clones = sorted(list(best_clones), key=lambda result: (result.get_clone().yield_count(), result.get_box().get_size()))
    for result in sorted_clones:
        result.print()

def read_from_csv():
    all_clones = CloneStorage()
    clones_file = open("clones.tsv", 'r')
    clones_reader = csv.reader(clones_file, delimiter="\t", quotechar='"')
    for row in clones_reader:
        count = int(row[1])
        cloneString = row[0]
        if count > 0:
            all_clones.add_clone(Clone.fromString(cloneString))
    return all_clones

def main():
    all_clones = read_from_csv()
    find_best(all_clones)

def main2():
    all_clones = read_from_csv()
    find_specific(all_clones)

if __name__ == "__main__":
    main()
