from context_menu import menus
import shutil

# not working https://github.com/saleguas/context_menu/issues/19
# fc = menus.FastCommand('cleanpdf', type='.pdf', command=shutil.which('cleanpdf') + ' "%1"')
fc = menus.FastCommand('cleanpdf', type='FILES', command=shutil.which('cleanpdf') + ' "%1"')
fc.compile()
