import rich

from rich.markdown import Markdown
# from pygments.lexers import PowershellLexer

rich.print(Markdown("```powershell\nNew-Alias tree rtree\n```"))