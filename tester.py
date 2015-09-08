import os, pdb, subprocess

result = subprocess.Popen(['python', '-m', 'scripts.test'], stdout=subprocess.PIPE).stdout.read()

