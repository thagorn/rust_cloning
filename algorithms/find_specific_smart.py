import sys
from box import Box
from utils.combinations import ncr
from utils.printer import ClonePathPrinter
from utils.progressbar import ProgressBar

class FindSpecificSmart:
    def __init__(self, all_clones, target, minimum_score):
        self.all_clones = all_clones
        self.current_generation = 0
        self.target = target
        self.minimum_score = minimum_score
        self.result = None
        self.done = False

    def _process(self, box):
        result = box.get_offspring()
        if result in self.all_clones.clones():
            return
        score = result.score()
        if (score == 30):
            if self.target.is_equivalent(result):
                self.result = result
                self.done = True
                return
        if score >= self.minimum_score:
            self.all_clones.add_clone(result)

    def run(self):
        while not self.done:
            self.current_generation += 1
            self._generation()

    def _generation(self):
        clones = list(self.all_clones.clones())
        num_clones = len(clones)
        pb = ProgressBar(ncr(num_clones, 4) + ncr(num_clones, 3))
        sys.stderr.write("Starting generation {} with {} clones\n".format(self.current_generation, num_clones))
        for i in range(num_clones):
            for j in range(i+1, num_clones):
                for k in range(j+1, num_clones):
                    for l in range(k+1, num_clones):
                        box = Box([clones[i], clones[j], clones[k], clones[l]], self.current_generation)
                        self._process(box)
                        if self.done:
                            return
                        pb.increment()

        for i in range(num_clones):
            for j in range(i+1, num_clones):
                for k in range(j+1, num_clones):
                    clone1 = clones[i]
                    clone2 = clones[j]
                    clone3 = clones[k]
                    box = Box([clones[i], clones[j], clones[k]], self.current_generation)
                    self._process(box)
                    if self.done:
                        return
                    pb.increment()
        pb.clear()

    def print(self):
        printer = ClonePathPrinter()
        printer.print_clone(self.result)
