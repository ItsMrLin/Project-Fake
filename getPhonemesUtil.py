import subprocess
import sys
import os.path

if len(sys.argv) != 4:
	print 'Failed: requires three arguments :('
	exit()

print 'Called with audio file: ', sys.argv[1], ', transcript file: ', sys.argv[2]
print 'Results will be written to ', sys.argv[3]
cmd = ['java', '-cp', 'bin/:lib/sphinx4-core-1.0-SNAPSHOT.jar', 'GetPhonemeUtil',
		sys.argv[1], sys.argv[2], sys.argv[3]]
subprocess.call(cmd)