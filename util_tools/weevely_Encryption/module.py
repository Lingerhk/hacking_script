'''
Created on 22/ago/2011

@author: norby
'''

from inspect import getargspec

class_name = 'Module'

class Module:
    '''Generic class Module to inherit'''
    
    visible = True
    
    
    
    def __init__(self, modhandler, url, password):
        
        self.modhandler = modhandler
        self.url = url
        self.password = password
        
        self.name = self.__module__[8:]
        
        
        self._probe()
    
    def mprint(self, str, importance = 5):

        # Considering also an empty self.modhandler.verbosity
        if not self.modhandler.verbosity or importance >= self.modhandler.verbosity[-1]:
            print str
        
    
    def _probe(self):
        pass
    
    def run(self, module_arglist = []):
        
        if not self.modhandler.interpreter:
            self.modhandler.load_interpreters()
                
        output = None
        check1, argdict = self.params.set_and_check_parameters(module_arglist, oneshot=True)
        
        if check1:
            check2, arglist = self.params.get_parameters_list(argdict)

            if check2:
                
                try:
                    output = self.run_module(*arglist)
                except ModuleException, e:
                    self.mprint('[!] [%s] Error: %s' % (e.module, e.error))
                    
                
        return output
    
    def _get_default_vector2(self):
        
        conf_vector = self.params.get_parameter_value('vector')
        vector = self.vectors.get_vector_by_name(conf_vector)
        
        if vector:
            return [ vector ]
        
        return []
    
class ModuleException(Exception):
    def __init__(self, module, value):
        self.module = module
        self.error = value
    def __str__(self):
        return '%s %s' % (self.module, self.error)