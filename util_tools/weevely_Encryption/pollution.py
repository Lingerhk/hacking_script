# -*- coding: utf-8 -*-
# This file is part of Weevely NG.
#
# Copyright(c) 2011-2012 Weevely Developers
# http://code.google.com/p/weevely/
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import base64, codecs
from random import random, randrange, choice, shuffle, randint
from collections import *


def random_string(charset = 'abcdefghijklmnopqrstuvwxyz', len=4, fixed=False):
	if not fixed:
		len = randrange(2,len)
	return ''.join([choice(charset) for i in xrange(len)])

def pollute_with_random_str(str, charset = '!"#$%&()*-,./:<>?@[\]^_`{|}~', frequency=0.3):

	str_encoded = ''
	for char in str:
		if random() < frequency:
			str_encoded += random_string(charset, 1, True) + char
		else:
			str_encoded += char
			
	return str_encoded
	
	
def pollute_replacing(str, charset = 'abcdefghijklmnopqrstuvwxyz'):
	
	# Choose common substring in str
	count = {}
	for r in range(1,len(str)):
		count.update( Counter(str[i:i+r] for i in range(len(str)-r-1)) )
	
	substr = choice(sorted(count, key=count.get, reverse=True)[:5])

	# Choose str to replace with
	pollution = find_randstr_not_in_str(str.replace(substr,''), charset)
			
	replacedstr = str.replace(substr,pollution)
	return substr, pollution, replacedstr

	
def find_randstr_not_in_str(str, charset):

	while True:

		pollution_chars = random_string(charset, 16, True)
			
		pollution = ''
		found = False
		for i in range(0, len(pollution_chars)):
			pollution = pollution_chars[:i]
			if (not pollution in str) :
				found=True
				break
			
		if not found:
			print '[!] Bad randomization, retrying.'
		else:
			return pollution

	
		
	
	
def pollute_with_static_str(str, charset = 'abcdefghijklmnopqrstuvwxyz', frequency=0.1):

	pollution = find_randstr_not_in_str(str, charset)
		
	str_encoded = ''
	for char in str:
		if random() < frequency:
			str_encoded += pollution + char
		else:
			str_encoded += char
			
	return pollution, str_encoded
