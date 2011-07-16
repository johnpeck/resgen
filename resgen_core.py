""" resgen_core.py
    Generates standard resistor symbols using the configuration found
    in resgen.conf.  Makes both a horizontal and a vertical version.
    Will not overwrite an exisiting symbol. """

# -------------------------- Pure Python -----------------------------
import math

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

""" makename(value, footprint_filename)
    Creates the filename from the value parameter and the footprint name
    -- Every value will have three significant figures. """
def makename(value, footprint_filename):
    value = float(value) # ensure it is a float, not a string

    if (value/1e6 >= 1):
        Mval = int(math.floor(value/1e6))
        kval = int(value - Mval*1e6)
        name = str(Mval) + 'M' + str(kval)
        while (len(name) > 4):
            name = name[0:-1] # Reduce to maximum of 3 significant figures
    elif (value/1e3 >= 1):
        kval = int(math.floor(value/1e3))
        rval = int(value - kval*1e3)
        name = str(kval) + 'k' + str(rval)
        while (len(name) > 4):
            name = name[0:-1] # Reduce to maximum of 3 significant figures
    elif (value >= 1):
        rval = int(math.floor(value))
        name = str(rval) + 'r'
        while (len(name) < 4):
            name = name + '0'
    elif (value < 1):
        mval = int(math.floor(value * 1000))
        name = str(mval) + 'm'
        while (len(name) < 4):
            name = name + '0'
    name = name + '_' + footprint_filename # Tack on the footprint name
    return name

""" makevalue(value, precision)
    Format the resistor value from the configuration file into the
    string shown on a schematic for a given precision.
    --- Three significant digits and the engineering character for the
        10x multiplier"""
def makevalue(value, precision):
    value = float(value) # ensure it is a float, not a string
    precision = int(precision) # ensure it is an int, not a string
    if (value/1e6 >= 1):
        Mval = int(math.floor(value/1e6))
        kval = int(value - Mval*1e6)
        valstr = str(Mval) + '.' + str(kval)
        while len(valstr) < (precision + 1):
            valstr += '0' # Pad to specified precision
        while len(valstr) > (precision + 1):
            valstr = valstr[0:-1] # Reduce to specified precision
        if valstr.endswith('.'):
            valstr = valstr[0:-1] # Get rid of the decimal point
        valstr += 'M'
    elif (value/1e3 >= 1):
        kval = int(math.floor(value/1e3))
        rval = int(value - kval*1e3)
        valstr = str(kval) + '.' + str(rval)
        while len(valstr) < (precision + 1):
            valstr += '0' # Pad to specified precision
        while len(valstr) > (precision + 1):
            valstr = valstr[0:-1] # Reduce to specified precision
        if valstr.endswith('.'):
            valstr = valstr[0:-1] # Get rid of the decimal point
        valstr += 'k'
    elif (value >= 1):
        rval = int(math.floor(value))
        valstr = str(rval)
        if len(valstr) < (precision + 1):
            valstr += '.'
        while len(valstr) < (precision + 1):
            valstr += '0' # Pad to specified precision
        while len(valstr) > (precision + 1):
            valstr = valstr[0:-1] # Reduce to specified precision
        if valstr.endswith('.'):
            valstr = valstr[0:-1] # Get rid of the decimal point
    elif (value < 1):
        mval = int(math.floor(value * 1000))
        valstr = '0.' + str(mval)
        while len(valstr) < (precision + 2):
            valstr += '0' # Pad to specified precision
        while len(valstr) > (precision + 2):
            valstr = valstr[0:-1] # Reduce to specified precision
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

