from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("D:\\code\\doc\\git\\git使用说明.md", 'r', encoding='utf-8') as readme:
    markdown = Markdown(readme.read())
console.print(markdown)