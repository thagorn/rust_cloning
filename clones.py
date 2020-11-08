import csv
from box import Box
from clone import Clone
from result import Result
from clonestorage import CloneStorage
from find_best import FindBest


def read_from_csv():
    all_clones = CloneStorage()
    clones_file = open("clones.tsv", 'r')
    clones_reader = csv.reader(clones_file, delimiter="\t", quotechar='"')
    for row in clones_reader:
        cloneString = row[0]
        all_clones.add_clone(Clone.fromString(cloneString))
    return all_clones

def main():
    all_clones = read_from_csv()
    find_best = FindBest(all_clones, 1, 1)
    find_best.run()
    find_best.print()

if __name__ == "__main__":
    main()
