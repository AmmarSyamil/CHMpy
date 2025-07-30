import os
from pathlib import Path
import stat
import subprocess
from textual import log, on
from pathlib import Path
from pprint import pprint
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Static, Label, Tree, Button, Input

from rich.pretty import Pretty
from typing import Union, TypedDict
from textual.containers import Vertical, Horizontal
from textual.message import Message
from textual.validation import Function, Number, ValidationResult, Validator


#path = Path(".")

class Data_format(TypedDict):
    type: str
    data: dict[str, list]
    sub: dict[str, "Data_format"]

Data_model = dict[str, Data_format]

class Message_tree_view(Message):
    print("dapet pesang kagn")
    def __init__(self, path_tree):
        super().__init__()
        self.path = path_tree

class Message_dir_data(Message): 
    print("message dir daata get")
    def __init__(self, data):
        super().__init__()
        self.data = data

class Launch_app(Static):

    CSS = """
    Launch_app {
    height: 3; /* Or whatever fits your layout nicely */
    }

    Input.-valid {
        border: tall $success 60%;
    }
    Input.-valid {
        border: tall $success 60%;
    }
    Input.-valid:focus {
        border: tall $success;
    }
    Input.-invalid {
        border: tall $error 60%;
    }
    Input.-invalid:focus {
        border: tall $error;
    }
    
    """
        
    def __init__(self):
        super().__init__()
        self.path: Path =  Path(".")
        self.data: Data_model = {}

    def on_mount(self):
        None

    def _process_input(self, input_widget: Input) -> None:
        input_value = input_widget.value.strip()

        if not input_widget.validators:
            print("no validator")
            return
        
        validator = input_widget.validators[0]
        result = validator.validate(input_value)
            
        
        if not result.is_valid:
            input_widget.remove_class("-valid")    # Remove the valid class
            input_widget.add_class("-invalid")
            print(f"Validation failed: {result.failure_descriptions}")  # Add debug
            return
        else:
            input_widget.remove_class("-invalid") # Remove the invalid class
            input_widget.add_class("-valid")
            print(f"Validation passed, sending message for: {input_value}")  # Add debug
            self.app.post_message(Message_tree_view(Path(input_value)))

    @on(Input.Submitted, "#dir_input_user")
    def on_dir_submitted(self, event: Input.Submitted) -> None:
        self._process_input(event.input)

    @on(Button.Pressed, "#show_dir_button")
    def on_dir_pressed(self, event: Button.Pressed) -> None:
        input_widget = self.query_one("#dir_input_user", Input)
        self._process_input(input_widget)

    # @on(Input.Submitted, "#dir_input_user")
    # def on_dir_submitted(self, event: Input.Submitted) -> None:
    #     if event.input.id == "dir_input_user":
    #         self.path = Path(event.input.value)


    # @on(Button.Pressed, "#show_dir_button")
    # def on_dir_pressed(self, event: Button.Pressed) -> None:
    #     print("masukkang")
    #     if event.button.id == "show_dir_button":
    #         print("masuk sini ")
    #         input_widget = self.query_one("#dir_input_user", Input)
    #         input_value = input_widget.value
    #         # input_value = self.path
    #         validator = input_widget.validators[0]
    #         result = validator.validate(input_value)
    #         if not result.is_valid:
    #             input_widget.remove_class("-valid")
    #             input_widget.add_class("-invalid")
    #             print("hitam ngak valid")
    #             return
    #         else:   
    #             input_widget.remove_class("-invalid")
    #             input_widget.add_class("-valid")
    #             print("miawmiaw on on on on on on")
    #             self.app.post_message(Message_tree_view(Path(input_value)))
        
    # def on_input_submitted(self, event: Input.Submitted):
    #     if event.input.id == "dir_input_user":
    #         self.path = Path(event.input.value)

    # def on_button_pressed(self, event: Button.Pressed):
    #     if event.button.id == "show_dir_button":
    #         input_widget = self.query_one("#dir_input_user", Input)
    #         input_value = input_widget.value
    #         # input_value = self.path
    #         validator = input_widget.validators[0]
    #         result = validator.validate(input_value)
    #         if not result.is_valid:
    #             input_widget.remove_class("-valid")
    #             input_widget.add_class("-invalid")
    #             return
    #         else:
    #             input_widget.remove_class("-invalid")
    #             input_widget.add_class("-valid")
    #             self.app.post_message(Message_tree_view(Path(input_value)))


    def set_data_dir(self, data):
        self.data = data

    def compose(self):
        with Vertical():
            yield Label("📁 Start CHMpy", id="title_label")
            with Horizontal():
                yield Button("✔ Load", id="show_dir_button")
                yield Input(
                    id="dir_input_user",
                    placeholder="Enter directory path...",
                    validators=[Validator_tree_view()],
                    validate_on=["submitted", "blur"]  # Only validate when submitted or losing focus
                )

    # @on(Input.Changed)
    # def show_invalid_reasons(self, event: Input.Changed) -> None:
    #     """Function to show the error log of the input for the data tree view"""
    #     # Updating the UI to show the reasons why validation failed
    #     if not event.validation_result.is_valid:
    #         self.query_one(Pretty).update(event.validation_result.failure_descriptions)
    #     else:
    #         self.query_one(Pretty).update([])

class Show_dir(Static):
    print("go show dir")
    def __init__(self, path: Path = None):
        super().__init__()
        self.data : Data_model = {}
        self.chmod_file: str
        self.perm_dict: dict = {}
        self.data_type: str
        self.tree_perm: Tree = Tree("Permission Tree")
        self.path: Path = path or Path('.')

    def show_tree(self, data_dict=None, parent_node=None):
        print("masuk show tree function")
        if data_dict is None:
            data_dict = self.data  
        if parent_node is None:
            parent_node = self.tree_perm.root  

        for key, value in data_dict.items():
            if value["type"] == "file":
                parent_node.add_leaf(f'{key}')
            else:
                new_branch = parent_node.add(f'{key}')
                if value.get("sub"):  
                    self.show_tree(value["sub"], new_branch)


    def get_permissions(self, chmod_str: str):
        """
        Function that return perm_dict and data_type of the fiven chmod_file like (drwxrwx).

        What it do is to translate those chmod format into human readeble list like this
        {
            "owner": {"chmod": "rwx", "data": ["read", "write", "execute"]},
            "group": {"chmod": "rwx", "data": ["read", "write", "execute"]},
            "others": {"chmod": "rwx", "data": ["read", "write", "execute"]},
        }
        """
        print("masuk get permissions")
        chmod = chmod_str
        data_type = chmod[0]
        if data_type == 'd':
            data_type = 'directory'
        elif data_type == '-':
            data_type = 'file'

        owner = chmod[1:4]
        group = chmod[4:7]
        others = chmod[7:10]

        perm_dict = {
            'owner': {
                'chmod':owner,
                'data': []
            },
            'group': {
                'chmod':group,
                'data': []
            }, 
            'others': {
                'chmod': others,
                'data': []
            }
        }


        for u in ['owner', 'group', 'others']:

            y = perm_dict[u]["chmod"]
            for i in range(len(y)):

                if y[i] == 'r':
                    perm_dict[u]["data"].append('read')
                elif y[i] == 'w':
                    perm_dict[u]["data"].append('write')
                elif y[i] == 'x':
                    perm_dict[u]["data"].append('execute') 

        self.perm_dict = perm_dict
        self.data_type = data_type
        return perm_dict, data_type

    def version_2(self):
        """function to return the dicttionary of the dir tree of the given path"""     
        print("masuk version 2")       

        def tree(dir_get, parent_dict, current_depth=0, max_depth=3, max_branch=20):
            if current_depth > max_depth:
                return
            
            #print(f'dir get {dir_get}')
            dir = Path(dir_get)
            #print(f'dir {dir}')
            if dir.name.startswith(".") and dir.name != "." or dir.name in {"__pycache__", ".venv", "venv", ".git"}:
                return
            counts = 0

            for subdir in dir.iterdir():
                if counts >= max_branch:
                    break
                if subdir.name.startswith("."):
                    continue
                
                mode = subdir.stat().st_mode
                permissions = stat.filemode(mode)
                data_get, file_type = self.get_permissions(permissions)

                #print(data_get)

                def itterate_data_get():
                    miaw = {}
                    for i in data_get:
                        something = data_get[i].get("data", [])
                        miaw.setdefault("data", {})[i] = something
                    return miaw
                

                node = {
                    "type": file_type,
                    "sub": {},
                    "data": itterate_data_get()["data"]
                }

                parent_dict[subdir.name] = node
                
                if subdir.is_dir():
                    
                    tree(subdir, node["sub"], current_depth +1, max_depth, max_branch)
                counts +=1


        tree(self.path, self.data)

        # input_widget = self.query_one("#dir_input_user", Input)
        # validator = input_widget.validator
        # if isinstance(validator, Validator_tree_view):
        #     validator.get_data_dir(self.data)

        #self.post_message(Message_dir_data(self.data))



    def on_mount(self):
        if hasattr(self, 'path') and self.path:
            self.version_2()
            self.show_tree()
        else:
            print("path not set yet")

    def compose(self):
        yield self.tree_perm

    # @on(Launch_app.Message_tree_view)
    # def start(self, message: Launch_app.Message_tree_view) -> None:
    #     if message:
    #         self.version_2()
    #         self.show_tree()

class Validator_tree_view(Validator):
    """class to validate the input sent before they gonna be processed to the next class"""
    print("validator masuk")
    # def __init__(self, data):
    #     super().__init__()
    #     self.data = data
    #     self.dir_data = {}
    def validate(self, value: str) -> ValidationResult:
        if self.is_valid(value):
            return self.success()
        else:
            return self.failure("somethings not right")
        
    # def get_data_dir(self, input_data):
    #     self.data = input_data

    @staticmethod
    def is_valid(value: str) -> bool:  # Fixed typo
        if not value or value.isspace():  # Empty/whitespace is invalid
            return False
        
        try:
            path = Path(value).expanduser().resolve()
            return path.exists() and path.is_dir()
        except (OSError, ValueError):  # Handle path errors
            return False

    # def on_mount(self):
    #     self.show_







class Main_app(App):
    CSS_PATH = "main.css"

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True, show=False),
        Binding("ctrl+x", "quit", "Quit", priority=True)
    ]

    def compose(self) -> ComposeResult:
        yield Launch_app()
        yield Vertical(id="main_container")
        #yield Show_dir()

    def on_mount(self):
        self.container = self.query_one("#main_container", Vertical)

    @on(Message_tree_view)
    def show_dir_view(self, message: Message_tree_view) -> None:
        print("dapet pesan masuk main apps")
        print(message.path)
        print("done??")

        self.container.remove_children()
        show_dir_widget = Show_dir(message.path)
        # show_dir_widget.version_2()
        # print("version 2 start")
        # show_dir_widget.show_tree()
        # print("show tree fucking star")

        self.container.mount(show_dir_widget)

    # @on(Message_dir_data)
    # def dir_data(self, message: Message_dir_data) -> None:

        



if __name__ == "__main__":
    app = Main_app()
    app.run()
