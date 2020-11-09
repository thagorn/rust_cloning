
class ClonePathPrinter:

    def print_clone(self, clone):
        generations = self._get_path_to_targets([clone], clone.get_box().get_generation())
        self._print_generations(generations)

    def _get_path_to_targets(self, targets, max_generation):
        generations = []
        for i in range(max_generation + 1):
            generations.append(set())
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

    def _print_generations(self, generations):
        for i in range(len(generations)):
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("Generation: %d" % (i))
            clones = list(generations[i])
            for clone in clones:
                clone.get_result().print()
