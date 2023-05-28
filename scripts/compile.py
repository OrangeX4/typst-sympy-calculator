import os

if __name__ == '__main__':
    # Get relative path of the root directory of the project
    rdir = os.popen('git rev-parse --git-dir').read()
    rel_path = os.path.dirname(rdir)
    # Change to that path and run the file
    if rel_path != '':
        os.chdir(rel_path)
    os.system('java -jar antlr-4.7.2-complete.jar TypstGrammar.g4 -o gen')