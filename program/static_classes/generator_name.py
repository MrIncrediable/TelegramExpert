import random
from collections import defaultdict


class GeneratorName:
    def __init__(self):
        self.male = ['Aaron', 'Adam', 'Adrian', 'Alex', 'Alexander', 'Andrew', 'Daniel', 'Ivan', 'Max']
        self.female = ['Anna', 'Daria', 'Elena', 'Maria', 'Sofia', 'Victoria']
        self.surname = ['Smith', 'Johnson', 'Brown', 'Ivanov', 'Petrov', 'Sidorov']

    def _transitions(self, names):
        transitions = defaultdict(list)
        for name in names:
            marked = '^' + name + '$'
            for left, right in zip(marked, marked[1:]):
                transitions[left].append(right)
        return transitions

    def _generate(self, names):
        transitions = self._transitions(names)
        chars = ['^']
        while len(chars) < 15:
            current = chars[-1]
            if current not in transitions:
                break
            char = random.choice(transitions[current])
            if char == '$':
                break
            chars.append(char)
        return ''.join(chars[1:])

    def first_name(self, sex=None):
        source = self.male if sex == 1 or sex == 'male' else self.female
        for _ in range(10):
            name = self._generate(source)
            if len(name) >= 5:
                return name
        return random.choice(source)

    def last_name(self):
        return self._generate(self.surname)

    def get(self):
        sex = random.randint(1, 2)
        return self.first_name(sex), self.last_name(), sex
