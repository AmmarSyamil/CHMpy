import os
from pathlib import Path
import stat
import subprocess
from textual import log
from pathlib import Path
from pprint import pprint
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Static, Label, Tree, Button
from rich.pretty import Pretty



class Main(App):
    def compose(self):
        tree = Tree("Dune")
        tree.root.expand()
        characters = tree.root.add("Characters", expand=True)
        characters.add_leaf("Paul")
        characters.add_leaf("Jessica")
        characters.add_leaf("Chani")
        characters = tree.root.add("miaw", expand=True)
        yield tree


if __name__ == "__main__":
    app = Main()
    app.run()
