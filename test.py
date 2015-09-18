import pdb, subprocess, sys
try:
  #os.system('python -m test.raise_error')
  result = subprocess.check_output(['python', '-m', 'test.raise_error'])
  pdb.set_trace()
except subprocess.CalledProcessError as e:
  print(e.output)
