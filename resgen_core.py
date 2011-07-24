""" resgen_core.py
    Generates standard resistor symbols using the configuration found
    in resgen.conf.  Makes both a horizontal and a vertical version.
    Will not overwrite an exisiting symbol. """

# -------------------------- Pure Python -----------------------------
import math
from decimal import *

def processconf(rawfile):
    resdict = {}
    for line in rawfile.split('\n'):
        if line.strip().startswith('value'):
            resdict['value'] = line.split('=')[1].strip()
        if line.strip().startswith('precision'):
            resdict['precision'] = line.split('=')[1].strip()
        if line.strip().startswith('part'):
            resdict['part'] = line.split('=')[1].strip()
        if line.strip().startswith('footprint'):
            resdict['footprint'] = line.split('=')[1].strip()
    return resdict
    

""" makename(value, precision, footprint_filename)
    Creates the filename from the value, precision, and the footprint 
    name. """
def makename(value, precision, footprint_filename):
    value = Decimal(value) # ensure it is a Decimal, not a string
    precision = int(precision) # ensure that precision is an integer
    getcontext().prec = precision # Set the precision for Decimal numbers
    
    if (value/Decimal(1e6) >= 1):
        Mval = Decimal(math.floor(value/Decimal(1e6)))
        kval = Decimal(math.floor(value - Mval*Decimal(1e6)))/Decimal(1e3)
        name = str(Mval) + 'M' + '%(number)03u' %{'number':kval}
    elif (value/Decimal(1e3) >= 1):
        kval = Decimal(math.floor(value/Decimal(1e3)))
        rval = Decimal(value - kval*Decimal(1e3))
        name = str(kval) + 'k' + '%(number)03u' %{'number':rval}
    elif (value >= 1):
        rval = Decimal(math.floor(value))
        mval = Decimal(math.floor((value - rval)*Decimal(1e3)))
        name = str(rval) + 'r' + '%(number)03u' %{'number':mval}
    elif (value < 1):
        mval = Decimal(math.floor(value * 1000))
        name = str(mval) + 'm'
    """ Format the name for the specified precision """
    while len(name) < (precision + 1):
        name += '0' # Pad to specified precision
    while len(name) > (precision + 1):
        if name.endswith(('M','k','r')):
            break
        else:
            name = name[0:-1] # Reduce to specified precision
    name = name + '_' + footprint_filename # Tack on the footprint name
    return name


""" zeropad(string,width)
    Adds zeros or removes characters from the right end of a string to
    make it the specified width. Removes any trailing decimal points."""
def zeropad(string,width):
    string = str(string)
    width = int(width)
    while len(string) < (width):
        string += '0' # Pad to specified precision
    while len(string) > (width):
        string = string[0:-1] # Reduce to specified precision
    if string.endswith('.'):
        string = string[0:-1] # Get rid of the decimal point
    return string

""" makevalue(value, precision)
    Format the resistor value from the configuration file into the
    string shown on a schematic for a given precision. """
def makevalue(value, precision):
    value = Decimal(value) # ensure it is a Decimal, not a string
    precision = int(precision) # ensure it is an int, not a string
    getcontext().prec = precision # Set the precision for Decimal numbers
    
    if (value/Decimal(1e6) >= 1):
        Mval = Decimal(math.floor(value/Decimal(1e6)))
        kval = Decimal((value - Mval*Decimal(1e6))/Decimal(1e3))
        valstr = str(Mval) + '.' + '%(number)03u' %{'number':kval}
        valstr = zeropad(valstr,precision + 1) # Add 1 for decimal point
        valstr += 'M'
    elif (value/Decimal(1e3) >= 1):
        kval = Decimal(math.floor(value/Decimal(1e3)))
        rval = Decimal(value - kval*Decimal(1e3))
        valstr = str(kval) + '.' + '%(number)03u' %{'number':rval}
        valstr = zeropad(valstr,precision + 1) # Add 1 for decimal point
        valstr += 'k'
    elif (value >= 1):
        rval = Decimal(math.floor(value))
        mval = Decimal(math.floor((value - rval)*Decimal(1e3)))
        valstr = str(rval) + '.' + '%(number)03u' %{'number':mval}
        valstr = zeropad(valstr,precision + 1) # Add 1 for decimal point
    elif (value < 1):
        mval = Decimal(math.floor(value * 1000))
        valstr = '0.' + '%(number)03u' %{'number':mval}
        valstr = zeropad(valstr,precision + 2) # Add 2 for point and zero
    return valstr

def processhorz(part, value, precision, footprint_name, template):
    """Construct a horizonal part"""
    return "".join([template,
                    'T 0 1300 8 10 0 0 0 0 1' + '\n', # Footprint
                    'footprint=' + footprint_name + '\n',
                    'T 0 1095 8 10 0 0 0 0 1' + '\n', # Part number
                    'part=' + part + '\n',
                    'T 1300 0 8 10 1 1 0 0 1' + '\n', # Value
                    'value=' + makevalue(value = value,
                                            precision = precision) + '\n',
                ])


def processvert(part, value, precision, footprint_name, template):
    """Construct a vertical part"""
    return "".join([template,
                    'T 0 1700 8 10 0 0 0 0 1' + '\n', # Footprint
                    'footprint=' + footprint_name + '\n',
                    'T 0 1495 8 10 0 0 0 0 1' + '\n', # Part number
                    'part=' + part + '\n',
                    'T 300 500 8 10 1 1 0 0 1' + '\n', # Value
                    'value=' + makevalue(value = value,
                                            precision = precision) + '\n',
                ])

