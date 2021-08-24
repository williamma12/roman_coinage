import re
import numpy as np
import pandas as pd
import sqlite3

def makeQuery(tableName, columns=['*'], conditions=[]):
    '''
    Parameters
    ----------
    tableName: str
        name of the table to get the data from
    columns: list
        list of the columns desired
    conditions: list
        list of the conditions (contained within a list) to filter the rows 
        
    Returns
    -------
    Returns a SQL query from the tableName with the columns and filtered by the conditions

    DocTests
    --------
    >>> makeQuery(foo)
    'SELECT * FROM foo'
    >>> makeQuery(bar, columns=['foo', 'car'], conditions=[['IN', 'col', 'yes']])
    'SELECT foo, car FROM bar WHERE col IN (?)
    '''
    cols = ', '.join(col for col in columns)
    conds = []
    if conditions != []:
        for cond in conditions:
            placeholder= '?'
            placeholders= ', '.join(placeholder for _ in cond[2])
            cond = cond[1] + ' ' + cond[0] + ' (' + placeholders + ')'
            conds.append(cond)
        conds = ' AND '.join(conds)
        conds = ' WHERE ' + conds
    else:
        conds = ''
    query = 'SELECT ' + cols + ' FROM ' + tableName + conds
    return query


def readQuery(fileName, tableName, columns=['*'], conditions=[]):
    cnx = sqlite3.connect('../Data/'+fileName)
    cursor = cnx.cursor()
    query = makeQuery(tableName, columns=columns, conditions=conditions)
    if conditions == []:
        cursor.execute(query)
    else:
        vals = []
        for cond in conditions:
            vals += cond[2]
        cursor.execute(query, vals)
        
    rows = cursor.fetchall()

    if columns == ['*']:
        columnNames = [description[0] for description in cursor.description]
        df = pd.DataFrame(rows)
        df.columns = columnNames
    else:
        df = pd.DataFrame(rows, columns=columns)
    
    return df


def stringToList(sep=', ', valType=str):
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
        if valType == int and result == '':
            return []
        else:
            return [valType(val) for val in result.split(sep)]

    return seperator


def listToString(sep=', '):
    '''
    Parameters
    ----------
    sep: str
        Seperator to seperate each item

    Returns
    -------
    Returns a string of the items of the list seperated by the seperator
    '''
    def combiner(lst):
        if len(lst) != 0:
            result = str(lst[0])
            for i in range(1, len(lst)):
                result += sep + str(lst[i])
        else:
            result = ''
        return result
    
    return combiner


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
    # Dict for mapping one name to another.
    replacements = {
            'Lyon': 'Lugdunum',
            'Londinium': 'London'
            }

    place = string.split('Minted in: ')[-1].strip()
    if place in replacements:
        place = replacements[place]
    place = ''.join(x for x in place if x.isalpha())
    return place


def getInscriptions(insc):
    '''
    Parameters
    ----------
    insc : list of dicts
        Data of the inscriptions

    Returns
    -------
    Returns a panads Series with columns 'Obverse legend' and 'Reverse legend'
    '''
    obverse = []
    reverse = []
    for i in insc:
        if 'Inscription Transliteration' in i:
            content = i['Inscription Transliteration']
        elif 'Inscription Content' in i:
            content = i['Inscription Content']
        else: 
            continue
        
        content = re.sub(r'[^\x00-\x7f]',r' ', content)
        if 'Inscription Position' in i:
            position = i['Inscription Position']
            if position == 'obverse':
                obverse.append(content)
            elif position == 'reverse':
                reverse.append(content)
    return pd.Series({'Obverse legend': obverse, 'Reverse legend': reverse})


def cleanInscriptions(df, col_name = 'Inscriptions'):
    '''
    Parameters
    ----------
    df : pandas Dataframe
        Dataframe contiaining data. Inscriptions should be put as a list of dicts
    col_name : str
        Column name of the inscriptions data
    
    Returns
    -------
    Returns dataframe with the columns 'Obverse legend' and 'Reverse legend'
    '''
    result = df.apply(lambda x: getInscriptions(x['Inscriptions']), axis=1)
    reuslt = df.drop(col_name, axis=1)
    return result

def cleanDescription(desc):
    """
    Parameters
    ----------
    desc : str
        String of the original description
        
    Returns
    -------
    Returns a description with just the description of the 
    obverse and reversed with only letters and spaces. Also
    removes extraneous words.
    
    DocTest
    -------
    >>> cleanDescription('Struck Silver. (obverse) Bust of Gallienus. (reverse) Concordia, draped, standing left.')
    'Gallienus Concordia draped standing'
    """
    lst = re.split(". \([a-z]+\)", desc)
    
    if len(lst) == 2:
        cleanedStr = lst[1]
    elif len(lst) == 3:
        cleanedStr = lst[1] + lst[2]
    else:
        cleanedStr = ""
    
    cleanedStr = re.sub(r'[^a-zA-Z ]+', '', cleanedStr)
    
    # Remove extraneous words
    extra_words = ['Bust', 'of', 'with', 'left', 'who', 'when', 'which', 'there', 'the']
    for word in extra_words:
        cleanedStr = cleanedStr.replace(word, '')
    
    return cleanedStr.strip()


def cleanDenomination(string):
    '''
    Parameter
    ---------
    string : str
        String containing the denomination of the coin.

    Return
    ------
    Returns the demonation string containing only letters

    Doctests
    --------

    '''
    string = string.split("|")[0]
    string = re.sub(r'[^a-zA-Z ]+', '', string).lower()
    return string


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
    if len(string) != 0:
        data = re.findall('^[^\(]+', string)[0].strip()
        return data
    else:
        return string


def makeDescription(material, manufacture, obverse, reverse):
    '''
    Parameters
    ----------
    material: str
        Coin's material content
    manufacture: str
        How the coin was made (ie struck)
    obverse: str
        Description of the obverse
    reverse: str
        Description of the reverse

    Returns
    -------
    Returns a string combining everything into one nice string
    '''
    result = manufacture + ' ' + material + '.'
    if obverse:
        result += ' (obverse) ' + obverse + '.'
    if reverse:
        result += ' (reverse) ' + reverse + '.'
    return result


def makeDupCheckCol(material, denomination, portrait, mint, year):
    '''
    Parameters
    ----------
    material: str
        Coin's material 
    denomination: str
        Coin's denomination
    portrait: type that can be cast into a str
        Portrait on the coin
    mint: str
        Mint of the coin
    year: type that can be cast into a str
        However formatted year as long as consistent throughout all entries

    Returns
    -------
    Concatenates material, denomination, portrait, mint, and year into one big
    string to check if the coin has a duplicate.
    '''
    result = (material + ' ' + denomination + ' ' + str(portrait) + ' ' 
            + mint + ' ' + str(year))
    return result


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
    result.columns = [col_name, 'Count']
    result = result.loc[result.sort_values(['Count'], ascending=False).index]
    return result


def cleanDF(df, lists, strings, floats, dates, redundant_notes, do_nothing, 
        dup_cols, production_place='Production place', denomination='Denomination'):
    '''
    Parameters
    ----------
    df : pandas dataframe 
        dataframe containing data to clean
    lists : list of str
        column names of the columns containing lists
    strings : list of str
        column names of the columns containing strings
    floats : list of str
        column names of the columns containing floats
    dates : list of str
        column names of the columns containing dates
    redundant_notes : list of str
        column names of the columns containing parenthses
    do_nothing : list of str
        column names of the columns to not touch but keep in final dataframe
    dup_cols : list of str
        column names of the columns to check for duplicate coins
    production_place : str
        column name of the production place data
    denomination : str
        column name of the denomination data
    
    Returns
    -------
    Returns a dataframe with corresponding input columns cleaned accordinly, the other columns removed, and 
    removing duplicate coins if all the values in columns dup_cols are the same.
    '''
    result = pd.DataFrame()
    for lst in lists:
        result[lst] = df[lst].apply(cleanList)
    for string in strings:
        result[string] = df[string].apply(cleanString)
    for flot in floats:
        result[flot] = df[flot].apply(float_conversion).replace(np.nan, -1)
    for date in dates:
        result[date] = df[date].apply(dateRange)
    for col in redundant_notes:
        result[col] = result[col].apply(removeNotes)
    for col in do_nothing:
        result[col] = df[col]
    try:
        result[production_place] = result[production_place].apply(cleanProductionPlace)
    except:
        result[production_place] = df[production_place].apply(cleanProductionPlace)
        
    # Reindex dataframe and remove duplicates
    result = result.reindex(sorted(result.columns), axis=1)
    result = (result.drop_duplicates(subset=dup_cols).reset_index(drop=True))
    result.loc[result[denomination] == '', denomination] = "?"
    return result


if __name__ == "__main__":
        import doctest
        doctest.testmod()
