# -*- coding: utf-8 -*-
# tellmeonce.py

import os
import os.path
import sys
from types import *

__version__ = '0.1.0'

def by_file(file_name, test_body, error_callback, restore_callback,
            exit_code=None, error_class=Exception):
    '''
    Tries the test_body and if it catches the given exception,
    it calls callback (if callback is a function) or writes 
    callback to stderr (if callback is a string), unless there
    is already file named file_name relative to the main script. 
    If exit_code is specified, the main script will then die
    with the specified code regardless of whether the named
    file. If no exception is caught and the named file exists,
    
    
    By default, this function will catch any Exception. This can
    be narrowed down with error_class. error_callback can
    optionally take this Exception instance as a lone parameter.
    '''
    
    ok_last_time = not os.path.isfile(file_name)
    
    try:
        test_body()
        # If the test failed last time, perform the callback/message
        # and delete the file:
        if not ok_last_time:
            if type(restore_callback) == FunctionType:
                restore_callback()
            else:
                sys.stderr.write(str(restore_callback))
            os.remove(file_name)
    except error_class as e:
        if ok_last_time:
            if type(error_callback) == FunctionType:
                # The callback can optionally take the error as an argument:
                try:
                    error_callback(e)
                except TypeError:
                    error_callback()
            else:
                sys.stderr.write(str(error_callback))
            open(file_name, 'w').close()
        if exit_code is not None:
            sys.exit(exit_code)