import re

def stringToList(sep=', '):
    '''
    Parameters
    ---------
    sep: str
        String that seperates the values in the list

    Returns
    ------
    Returns a function that takes in a string and returns a list

    Doctest
    ------
    >>> stringToList(', ')('[one, 2, III]')
    ['one', '2', 'III']
    '''

    def seperator(string):
        result = string.strip('[]{}')
        return result.split(sep)

    return seperator


def stringToListofDicts(list_sep, dict_sep, key_sep): 
    '''
    Parameters
    ----------
    list_sep: str
        Character that seperates the dictionaries

    dict_sep: str
        String that seperates the key-value pairs

    key_sep: str
        String that seperates the key and value within the key-value pairs
    
    Returns
    -------
    Returns a function that takes in the string and returns a dictionary

    Doctest
    -------
    >>> stringToListofDicts('|', ';', ':')('1:one;2:two|1:I;2:II')
    [{'2': 'two', '1': 'one'}, {'2': 'II', '1': 'I'}]
    '''
    def seperator(string):
        result = []
        parts = string.split(list_sep)
        
        for part in parts:
            subparts = part.split(dict_sep)
            dic = {}
            for subpart in subparts:
                try:
                    content = subpart.split(key_sep)
                    dic[content[0]] = content[1]
                except:
                    pass
            result.append(dict(dic))
        
        return result
    return seperator


def cleanString(string):
    '''
    Parameters
    ----------
    string: str
        String that needs to be cleaned
    
    Returns
    -------
    Removes the descriptor and returns the (assumed) description
    
    Doctests
    --------
    >>> cleanString('Named in inscription & portrayed: Julius Caesar(probably)')
    'Julius Caesar'
    >>> cleanString('Ruler: Augustus (Octavian) (?)')
    'Augustus (Octavian)'
    >>> cleanString('dupondius    (?)          ')
    'dupondius'
    '''
    remove_items = ['(?)', '(probably)']
    result = string
    
    for substr in remove_items:
        result = result.replace(substr, '')
    
    if ':' in result:
        result = [s for s in result.split(':')][1]
    return result.strip()


def cleanList(lst):
    '''
    Parameters
    ----------
    lst: Python list
        list of strings to be cleaned
    
    Returns
    -------
    Tuple of cleaned strings
    
    Doctests
    --------
    >>> cleanList(['Ruler: Augustus (Octavian) (?)'])
    ('Augustus (Octavian)',)
    >>> cleanList(['Ruler:Augustus (Octavian)(?)', 'Moneyer:P Lurius Aggrippa'])
    ('Augustus (Octavian)', 'P Lurius Aggrippa')
    >>> cleanList(['symbol', 'emperor/empress'])
    ('symbol', 'emperor/empress')
    '''
    return tuple([cleanString(x) for x in lst])


def dateRange(date):
    '''
    Parameter
    ---------
    date: str
        Date range given as a string
    
    Returns
    -------
    Returns list of the date range
    
    Doctests
    --------
    >>> dateRange('27BC-14 (?)')
    (-27, 14)
    >>> dateRange('44BC (cira) -40BC')
    (-44, -40)
    >>> dateRange('4-14')
    (4, 14)
    '''
    dates = date.split('-')
    result = []
    
    for year in dates:
        certain = True
        bc = 'BC' in year
        try:
            year = int(re.sub('[^\d]', '', year))
        except:
            break
        if bc:
            year = 0 - year
        result.append(year)
        
    return tuple(result)
        

def float_conversion(x):
    '''
    Parameter
    ---------
    x: str
        Input value
    
    Return
    ------
    Returns the float or 0 if empty string
    '''
    try:
        x = float(x)
    except:
        x = 0
    return x


def cleanProductionPlace(string):
    '''
    Parameter
    ---------
    string: str
        Input string formatted as following:
            * Minted in: (place here)
            * Minted in: (place here) Minted in: (place here)
    
    Return
    ------
    Returns the production place with the 'Minted in: ' filtered out. If
    multiple production places listed, returns the last one.
    
    Doctests
    --------    
    >>> cleanProductionPlace('Minted in: Gaul (Cisalpine) (Europe,Gaul) Minted in: Italy (Europe,Italy) ')
    'Italy (Europe,Italy)'
    >>> cleanProductionPlace('Minted in: Gaul (Cisalpine) ')
    'Gaul (Cisalpine)'
    '''
    place = string.split('Minted in: ')[-1].strip()
    if place == 'Lyon': 
        place = 'Lugdunum'
    return place


def removeNotes(string):
    '''
    Parameter
    ---------
    string: str
        Input string with notes in parenthesis
        
    Return
    ------
    String with data without notes
    
    Doctests
    --------
    >>> removeNotes('Calagurris (Europe,Spain,Calahorra,Calagurris (city - archaic))')
    'Calagurris'
    >>> removeNotes('aureus (cut half)')
    'aureus'
    '''
    data = re.findall('^[^\(]+', string)[0].strip()
    return data


def prepareDataframeForMapping(df, col_name='Production place'):
    '''
    Parameters
    ----------
    df : Pandas Dataframe
        Dataframe containing data
    col_name : str
        Column name to get counts of for map

    Return
    ------
    Returns a pandas dataframe of columns col_name and 'Count' to be passed
    into the function makeMap in the file BokehMaker.py
    '''
    result = df.groupby([col_name]).size().reset_index()
    result.columns = ['Production place', 'Count']
    result = result.loc[result.sort_values(['Count'], ascending=False).index]
    return result


if __name__ == "__main__":
        import doctest
        doctest.testmod()
