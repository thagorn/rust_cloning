class Result:
    def __init__(self, clone, box):
        self.clone = clone
        self.box = box
        self.has_box = box != None

    def __eq__(self, other):
        if self.has_box and other.has_box:
            return self.clone == other.clone and self.box.get_size() == other.box.get_size()
        if self.has_box or other.has_box:
            return False
        return self.clone == other.clone

    def __hash__(self):
        if self.has_box:
            return 7 * self.box.get_size() + 19 * hash(self.clone)
        return 19 * hash(self.clone)

    def get_clone(self):
        return self.clone

    def get_box(self):
        return self.box

    def print(self):
        print("********")
        if not self.has_box:
            print("Start with the following clone:")
            print(self.clone)
        else:
            print("To get this clone:")
            print(self.clone)
            print("Use these parents:")
            for parent in self.box.get_parents():
                print(parent)
