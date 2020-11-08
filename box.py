from clone import Clone
from constants import RED_GENES, UNDEFINED_RED, UNDEFINED_GREEN

class Box:
    def __init__(self, clones, generation):
        self.parents = clones
        self.offspring = self._generate_offspring()
        self.size = len(self.parents)
        self.generation = generation

    def _generate_offspring(self):
        offspring = []
        for position in range(6):
            genes_seen = set()
            double = None
            result = None
            for clone in self.parents:
                gene = clone.get_genes()[position]
                if gene in genes_seen:
                    if double == None:
                        double = gene
                    elif double != gene:
                        if gene in RED_GENES:
                            if double in RED_GENES:
                                double = UNDEFINED_RED
                            else:
                                double = gene
                        elif double not in RED_GENES:
                            double = UNDEFINED_GREEN
                    result = double
                if result == None and gene in RED_GENES:
                    result = gene
                genes_seen.add(gene)
            if result == None:
                result = UNDEFINED_GREEN
            offspring.append(result)
        return Clone(offspring, self)

    def get_parents(self):
        return self.parents

    def get_offspring(self):
        return self.offspring

    def get_size(self):
        return self.size

    def get_generation(self):
        return self.generation
