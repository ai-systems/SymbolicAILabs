from trimlogic.term import Atom

def assertFollows(arg0, arg1=None):
    msg, term = None, None
    if isinstance(arg0, str):
        msg = arg0
        term = arg1
    else:
        term = arg0
    for x in fol_bc_ask([term], {}):
        print('Passed')
        return True
    if msg:
        print(message)
    else:
        print('Error')
        
def print_rules(predicate):
    print ""
    print "Rules for", predicate, ":"
    for rule in predicate.rules:
        print str(rule)
        

class Temperature(Atom):
    def __init__(self, name):
        Atom.__init__(self, str(name))

        
class Carbon(Atom):
    def __init__(self, name):
        Atom.__init__(self, str(name))