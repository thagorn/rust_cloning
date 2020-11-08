class CloneStorage:
    def __init__(self):
        self.all_clones = set()
        self.seen = set()

    def add_clone(self, new_clone):
        clone_hash = hash(new_clone)
        if clone_hash in self.seen:
            return
        self.seen.add(clone_hash)
        if new_clone.is_undefined():
            return
        self.all_clones.add(new_clone)

    def clones(self):
        return self.all_clones

    def size(self):
        return len(self.all_clones)
    
    def get_equivalent(self, clone_other):
        for clone in self.all_clones:
            if clone.is_equivalent(clone_other):
                return clone
        return None
