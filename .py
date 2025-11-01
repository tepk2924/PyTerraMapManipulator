import sys

sys.stdout.write('Hello World!')
sys.stdout.write('\x1b[6D') # move cursor left by 6 columns
sys.stdout.write('my World!')