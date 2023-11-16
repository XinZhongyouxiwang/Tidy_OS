class ParsingTypeA:
    def __init__(self, command: str, d_map):
        self.command = command
        self.map_dict = d_map

    def operate(self):
        for i in self.command.split(' '):
            if i in map_dict:
                self.map_dict[i]()


class ParsingTypeB(ParsingTypeA):
    def __init__(self, command: str, d_map: dict):
        super().__init__(command, d_map)

    def operate(self):
        for i in self.command.split(' '):
            if i in self.map_dict:
                self.map_dict[i]()


class ParsingTypeC(ParsingTypeB):
    def __init__(self, command: str, d_map):
        super().__init__(command, d_map)

    def operate(self):
        pass
    

if __name__ == '__main__':
    def print_a():
        print('a')


    map_dict = {'a': print_a}
    a = ParsingTypeA('a', map_dict)
    a.operate()
