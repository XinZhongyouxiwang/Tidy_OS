<<<<<<< HEAD
import keyboard
from rich.console import Console

console = Console()


class Select:
    def __init__(self, title, options):
        self.title = title
        self.options = options
        self.n_select = 0
        self.a = 1

    def up(self):
        if self.n_select > 0:
            self.n_select -= 1
        self.display()

    def down(self):
        if self.n_select < len(self.options) - 1:
            self.n_select += 1
        self.display()

    def display(self):
        console.clear()
        console.print(self.title + '(使用上下键选择)', justify='center')
        for l, c in enumerate(self.options):
            if l == self.n_select:
                console.print(f'{l + 1}. {c}', justify='center', style='#FF9933')
            else:
                console.print(f'{l + 1}. {c}', justify='center')

    def select(self):
        self.display()
        keyboard.add_hotkey('up', self.up)
        keyboard.add_hotkey('down', self.down)
        keyboard.wait('enter', True)
        return self.n_select

    def number(self):
        return self.select() + 1

    def content(self):
        return self.options[self.select()]


class Select_YN(Select):
    def __init__(self, title, default=True):
        self.default = default
        if default:
            super().__init__(title, ['Yes', 'no'])
        else:
            super().__init__(title, ['No', 'yes'])

    def number(self):
        if self.content() == 'Yes':
            return True
        else:
            return False


if __name__ == '__main__':
    a = Select_YN('A')
    console.print(a.number())
=======
>>>>>>> redeploy
