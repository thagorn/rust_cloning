from box import Box
from result import Result

class FindBest:
    def __init__(self, all_clones):
        self.all_clones = all_clones
        self.best_score = -100
        self.best_clones = set()

    def _process(self, box):
        result = box.get_offspring()
        if result in self.all_clones.clones():
            return
        score = result.score()
        if score > self.best_score:
            self.best_score = score
            self.best_clones = set()
        if score == self.best_score:
            resultBox = Result(result, box)
            self.best_clones.add(resultBox)

    def run(self):
        clones = list(self.all_clones.clones())
        num_clones = len(clones)
        for i in range(num_clones):
            for j in range(i, num_clones):
                for k in range(j, num_clones):
                    for l in range(k, num_clones):
                        box = Box([clones[i], clones[j], clones[k], clones[l]], 1)
                        self._process(box)

        for i in range(num_clones):
            for j in range(i, num_clones):
                for k in range(j, num_clones):
                    clone1 = clones[i]
                    clone2 = clones[j]
                    clone3 = clones[k]
                    box = Box([clones[i], clones[j], clones[k]], 1)
                    self._process(box)

    def print(self):
        sorted_clones = sorted(list(self.best_clones), key=lambda result: (result.get_clone().yield_count(), result.get_box().get_size()))
        for result in sorted_clones:
            result.print()
