import os

import questionary

from rich import print
from rich.columns import Columns
from rich.panel import Panel
from rich.align import Align
from rich.markdown import Markdown
from rich.box import HEAVY
from rtree._icons import default_file_icon, default_folder_icon, folder_icons, named_icons, icons

def show_alias_instructions():

    shell = get_shell()

    instructions_mapping  = {
        "cmd": """Create a file and make sure that file is in PATH, the easiest way is to just create the file
inside the `C:\Windows\System32` directory. And name the file `tree.bat`, then paste the following code into the file:

```bat
@echo off
call rtree%*
```""",

        **dict.fromkeys(["pwsh", "powershell"], """Open your powershell profile file (to get path run `echo $profile`) and paste the following code into the file:
```powershell
New-Alias tree rtree
```"""),

        **dict.fromkeys(["bash", "zsh"], f"""Open your {shell} profile file (path should be `~/{shell}rc`) and paste the following command:
```bash
alias tree="rtree"
```""")
    }

    print(Markdown(instructions_mapping.get(shell, f"**Search on google for how to add aliases to [red]{shell}[/]**"), inline_code_lexer="shell"))



def provide_default_shell():
    if os.name == 'posix':
        return os.environ['SHELL']
    elif os.name == 'nt':
        return os.environ['COMSPEC']
    raise NotImplementedError(f'OS {os.name!r} support not available')

def get_shell():
    import shellingham

    try:
        shell = shellingham.detect_shell()[0]
    except shellingham.ShellDetectionFailure:
        shell = provide_default_shell()
    return shell

def show_all_icons():
    all_icons = {}

    for i in (
        default_file_icon,
        default_folder_icon,
        *folder_icons.values(),
        *named_icons.values(),
        *icons.values()
    ):
        all_icons.update([tuple(i.values())])

    formatted_icons = []
    for icon, color in all_icons.items():
        formatted_icons.append(Panel(f"[{color}]{icon}[/]"))

    print(Panel(Columns(formatted_icons, align="center"), box=HEAVY, title="[b]All Icons[/]"))

def main():
    show_all_icons()
    works = questionary.confirm("Do all these icons work correctly?").ask()
    if not works:
        print(
            "[yellow]Please install the latest version of a compatible font from the nerd fonts website "
            "[magenta]<https://www.nerdfonts.com/font-downloads>[/] or make your own from "
            "[magenta]<https://github.com/ryanoasis/nerd-fonts#font-patcher>[/][/]")
    wants_alias = questionary.confirm("Do you want to automatically alias tree to rtree? (Not recommended)").ask()
    if wants_alias:
        show_alias_instructions()
    print("[bright_black]⮞[/] [b]For more help, please read the documentation at [/][cyan]https://wasi-master.github.io/rich-tree[/]")

if __name__ == "__main__":
    main()
