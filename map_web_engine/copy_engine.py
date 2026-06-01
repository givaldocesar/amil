import os, shutil

def copy_engine(output_dir, engine):
    current_dir = os.path.dirname(__file__)
    plugin_root = os.path.abspath(os.path.join(current_dir, '..'))
    src = os.path.join(plugin_root, 'assets', engine)
    dst = os.path.join(output_dir, engine)
    
    if not os.path.exists(dst):
        shutil.copytree(src, dst)