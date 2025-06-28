class State:
    def __init__(self):
        self.right_bank = set()
        self.left_bank = set()
        self.history = []
        self.torch_on_the_right = True
        self.duration = 0

    def is_final(self):
        return len(self.right_bank) == 0

    def child(self):
        child = State()
        child.right_bank = self.right_bank.copy()
        child.left_bank = self.left_bank.copy()
        child.history = self.history.copy()
        child.torch_on_the_right = not self.torch_on_the_right
        return child

    def calc_duration(self):
        for i in self.history:
            self.duration += max(i[0], i[1])
        return self.duration

    def children(self):
        children = []
        if self.torch_on_the_right:
            people_on_the_right = list(self.right_bank)
            size = len(people_on_the_right)
            for i in range(0, size-1):
                for j in range(i+1, size):
                    a = people_on_the_right[i]
                    b = people_on_the_right[j]
                    child = self.child()
                    child.right_bank.remove(a)
                    child.right_bank.remove(b)
                    child.left_bank.add(a)
                    child.left_bank.add(b)
                    child.history.append((a, b))
                    children.append(child)
        else:
            for i in self.left_bank:
                child = self.child()
                child.left_bank.remove(i)
                child.right_bank.add(i)
                child.history.append((i, 0))
                children.append(child)
        return children


def search(state, solutions):
    if state.is_final():
        solutions.append(state)
        return

    for child in state.children():
        search(child, solutions)


def main():
    initial_state = State()
    for i in [1, 2, 7, 10]:
        initial_state.right_bank.add(i)

    solutions = []
    search(initial_state, solutions)

    min_duration = 10_000
    min_solution = None
    for i in solutions:
        duration = i.calc_duration()
        if duration < min_duration:
            min_duration = duration
            min_solution = i.history

    print(min_solution)
    print(min_duration)


if __name__ == '__main__':
    main()

