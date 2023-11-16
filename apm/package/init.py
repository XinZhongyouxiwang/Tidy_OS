import rich, os, platform, datetime, keyboard

on_system = platform.system()

if on_system == 'Windows':
    index_path = os.path.normpath('/'.join(os.path.dirname(__file__).split('\\')[0:-1]))
    index_path_list = index_path.split('\\')
    index_path_list = index_path_list[0:index_path_list.index('Tterminal') + 1]
    import_path = '\\'.join(index_path_list)
elif on_system == 'Linux':
    index_path = os.path.normpath('/'.join(os.path.dirname(__file__).split('/')[0:-1]))
    index_path_list = index_path.split('/')
    index_path_list = index_path_list[0:index_path_list.index('Tterminal') + 1]
    import_path = '/'.join(index_path_list)
else:
    index_path = None
