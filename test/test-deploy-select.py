from rich.console import Console
console = Console()
import keyboard

u_select = 0
a = 0

def up(title, options:list):
    global u_select, a
    if a == 0:
        console.clear()
        if u_select >= 0 and u_select < len(options)-1:
            
            u_select += 1
            console.clear()
            console.print(u_select)

            # print(u_select)
        console.print(title, justify='center')
        for c, l in zip(options, range(len(options))):
            if u_select == l:
                
                console.print(f'{l+1}. {c}', style='#FF9933', justify='center')
            else:
                console.print(f'{l+1}. {c}',justify='center')

def down(title, options:list):
    global u_select, a
    if a == 0:
        console.clear()
        if u_select <= len(options)-1 and u_select > 0:
            u_select -= 1
            console.clear()
            # print(u_select)
        console.print(title, justify='center')
        for c, l in zip(options, range(len(options))):
            if u_select == l:
                console.print(f'{l+1}. {c}', style='#FF9933', justify='center')
            else:
                console.print(f'{l+1}. {c}', justify='center')
    
def select(title: str, options: list):
    global u_select
    a = 0
    console.clear()
    console.print(title, justify='center')
    for c, l in zip(options, range(len(options))):
        console.print(f'{l+1}. {c}', justify='center')
    
    # keyboard.add_hotkey('up', up, args=(title, options, ))
    # keyboard.add_hotkey('down', down, args=(title, options, ))
    keyboard.add_hotkey('up', up, args=(title, options, ))
    keyboard.add_hotkey('down', down, args=(title, options, ))
    keyboard.wait('enter', True)
    console.print(u_select)
if __name__ == '__main__':
    select('Hello', ['a', 'b'])
