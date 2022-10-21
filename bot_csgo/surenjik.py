class Bell:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def print_info(self):
        output1 = [f'{i}: {self.kwargs[i]}' for i in self.kwargs]
        output1.sort()
        print(*output1, sep=', ', end='')
        if len(self.args) == 0:
            if len(self.kwargs) == 0:
                print('-')
            else:
                print()
        else:
            if len(output1) != 0:
                print(';', end=' ')
            print(*self.args, sep=', ')


class BigBell(Bell):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flag = 1

    def sound(self):
        if self.flag == 1:
            print('ding')
            self.flag = 2
        else:
            print('dong')
            self.flag = 1


class LittleBell(Bell):
    def sound(self):
        print('ding')
