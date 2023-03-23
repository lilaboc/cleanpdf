from context_menu import menus
import shutil

fc = menus.FastCommand('cleanpdf', type='.pdf', command=shutil.which('cleanpdf') + ' "%1"')
fc.compile()
