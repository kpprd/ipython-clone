#!/usr/bin/python2
namespace = vars().copy()
if 'counter' not in namespace:
    namespace['counter']=0
if 'history' not in namespace:
    namespace['history']=[]
import sys
import subprocess
from StringIO import StringIO
import cPickle as pickle
import inspect

def feedline(input_string):
    """
    Executes a string as python code.
    Args:
        input_string (string): the string to be executed.
    Returns:
        the result of the execution formatted so as to resemble the output of IPython
    Example usage:
    >>> print feedline("5+5")
    Out [1]: 10
    In [1]:
    """
    input_string=str(input_string)
    output=""
    if len(input_string)>0 and input_string[0]=="!": # passes the command to the operating system if prefixed with an exclamation mark
        pop=subprocess.Popen(input_string[1:], stderr=subprocess.PIPE, shell=True, stdout=subprocess.PIPE).communicate()
        output=pop[0]+pop[1]
        namespace['counter']+=1
        output = str(output) + "In ["+str(namespace['counter'])+"]: "
    elif len(input_string)>6 and input_string[:6]=="%save ": # saves history using pickle if prompted by a '%save ' prefix
        file=open(input_string[6:], 'w')
        pickle.dump(namespace['history'], file)
        file.close()
        namespace['counter']+=1
        output = str(output) + "In ["+str(namespace['counter'])+"]: "
    else:
        try:
            if len(input_string)>1 and input_string[-1]=="?": # returns docstring if prompted by a ? suffix
                if input_string[:-1] in namespace:
                    namespace['counter']+=1
                    output= inspect.getdoc(namespace[input_string[:-1]]) + "\nIn ["+str(namespace['counter'])+"]: "
                else: # returns error message if object is not found
                    namespace['counter']+=1
                    output= 'Error: object {0} not found'.format(input_string[:-1]) + "\nIn ["+str(namespace['counter'])+"]: "
            else: # tries to evaluate using eval()
                output = eval(input_string, namespace)
                if input_string !="":
                    namespace['counter']+=1
                output = "Out [{0}]: {1}\nIn [{0}]: ".format(namespace['counter'], output)
        except SyntaxError: # if syntax error, try exec()
            oldio, sys.stdout = sys.stdout, StringIO()
            try:
                exec(input_string, namespace)
            except:
                print "Error: " + str(sys.exc_info()[1])
            # Get stdout buffer
            output = sys.stdout.getvalue()
            # Reset stdout
            sys.stdout = oldio
            if input_string !="": # add 1 to counter if input_string is not empty
                namespace['counter']+=1
            output = str(output) + "In ["+str(namespace['counter'])+"]: "
        except: # returns an appropriate error message if an error occurs
            namespace['counter']+=1
            output = "Error: " + str(sys.exc_info()[1]) + "\nIn [{0}]: ".format(namespace['counter'])
    namespace['history'].append(input_string)
    return output

def return_counter():
    """
    Returns the counter
    """
    return namespace['counter']


    
            
    