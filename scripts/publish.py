import os

def delete_path_recursively(root: str):
    if os.path.exists(root):
        for file in os.listdir(root):
            file_path = os.path.join(root, file)
            if os.path.isdir(file_path):
                delete_path_recursively(file_path)
            else:
                os.remove(file_path)
        os.rmdir(root)

if __name__ == '__main__':
    # Get relative path of the root directory of the project
    rdir = os.popen('git rev-parse --git-dir').read()
    rel_path = os.path.dirname(rdir)
    # Change to that path and run the file
    if rel_path != '':
        os.chdir(rel_path)
    # remove old wheels by delete ./dist/*
    delete_path_recursively('./dist')
    os.system('python setup.py bdist_wheel')
    os.system('twine upload dist/*')