import re
str1='<?php          aaaaaaaaaa <?php fdf?>  d  ?>'
# str1=str1.replace('<?php','').replace('?>','')
s=re.search('\?>$',str1)
print s
str2=re.sub('\?>$', '', str1)     
print str2

