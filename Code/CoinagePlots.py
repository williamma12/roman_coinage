import pandas as pd
import BokehPlots as bp
import CleanData as cd
from bokeh.plotting import show
from bokeh.models import Range1d, HoverTool
from bokeh.palettes import linear_palette, viridis, grey
from bokeh.layouts import gridplot

def coinsFromDates(df, date_range, col_name='date'):
    '''
    Parameters
    ----------
    df : Pandas dataframe
        Dataframe containing coins and dates
    date_range : tuple
        Tuple of length two containing date range
    col_names : str
        Column name of dates
        
    Return
    ------
    Returns a dataframe containing only the rows that have the correct dates
    '''
    begin = date_range[0]
    end = date_range[1]
    def intWithinTupleRange(tup):
        in_range = False
        if len(tup) == 1:
            if tup[0] >= begin and tup[0]<= end:
                in_range = True
        elif len(tup) == 2:
            if tup[0] >= begin and tup[1]<= end:
                in_range = False
        return in_range
    return df[df.apply(lambda x: intWithinTupleRange(x[col_name]), axis=1)]


def containKeyword(df, keys, col_names):
    '''
    Parameters
    ----------
    df : Pandas dataframe
        Dataframe containing coincs and column to look for keyword in
    keys : list
        list of strings to look for in each row of given column
    col_name : list
        list of columns of where to search for keyword in 'keys' list, respectively
    
    Return
    ------
    Returns a dataframe containing only rows that have the keyword in the given column
    '''
    def containIn(obj, key):
        contained = False
        cleaned_key = key.lower()
        
        if type(obj) == str:
            if cleaned_key in obj.lower():
                return True
        elif type(obj) == tuple or type(obj) == list:
            for item in obj:
                if cleaned_key in item.lower():
                    contained = True
                    break
                    
        return contained
    
    if len(keys) != len(col_names):
        raise ValueError('length of keys does not equal length of columns')
        
    for i, key in enumerate(keys):
        if key == keys[0]:
            try:
                result = df[df.apply(lambda x: containIn(x[col_names[0]], keys[0]), axis=1)]
                df = df.drop(df[df.apply(lambda x: containIn(x[col_names[0]], keys[0]), axis=1)], axis=1)
            except:
                raise ValueError('Missing keys')
        else:
            result.append(df[df.apply(lambda x: containIn(x[col_names[i]], key), axis=1)])
            df = df.drop(df[df.apply(lambda x: containIn(x[col_names[i]], key), axis=1)], axis=1)
            
    return result


def makeTitle(dates, subject):
    '''
    Parameters
    ----------
    dates : tuple
        tuple of length two with date range
    subject : list
        list of strings of the subjects
        
    Return
    ------
    Returns a string of an appropriate title
    
    Doctest
    -------
    >>> makeTitle([-44, -31], ['star'])
    "'Star' in coinage from 44BC to 31BC"
    '''
    result = ''
    str_dates = []
    for i, sub in enumerate(subject):
        result += "'" + sub[0].upper() + sub[1:] + "'"
        if len(subject) > 1:
            if i != len(subject)-1:
                result += ', '
            if i == len(subject) - 2:
                result += 'and '
                
    result += ' in coinage from '
    
    for date in dates:
        if date < 0:
            str_dates.append(str(abs(date)) + 'BC')
        else:
            str_dates.append(str(date) + 'BC')
    
    result += str_dates[0] + ' to ' + str_dates[1]
    return result


def makeCoinageStackedBar(df, title='', mint_col='mint', denom_col='denomination', y_label='Location Counts',
                   y_range=(0, 500), legend_location = 'top_right', plot_size=('responsive',), colors=grey):
    '''
    '''
    bar_plot = bp.makeStackedBar(df, mint_col, denom_col, sort_bars=True,
                               bars_ascending=False, sort_stacks=True, stacks_agg='sum', stacks_ascending=False,
                              colors=colors, title=title, plot_size=plot_size)

    bar_plot.yaxis.axis_label=y_label
    bar_plot.y_range = Range1d(y_range[0], y_range[1], bounds=y_range)
    bar_plot.legend.location = legend_location
    bar_plot.add_tools(HoverTool(tooltips=[('Denomination', '@denomination'), 
                                           ('Denomination Count', '@height'),
                                           ('Location Count', '@Sum')]))

    return bar_plot


def makeCoinageMap(df, title='', mint_col='mint', x_ranges=(-2.0e6, 5e6), y_ranges=(3.5e6, 7e6),
                   pt_size=lambda x: x, colors_ascending=False):
    '''
    '''
    counts = cd.prepareDataframeForMapping(df, col_name=mint_col)

    map_plot = bp.makeMap(counts, mint_col, 'Count', x_ranges=x_ranges, y_ranges=y_ranges, 
                          mintsFile='../GeoJSON/mints.geojson', path='../GeoJSON/', ext='html', 
                          pt_size=pt_size, colors_ascending=colors_ascending)
    return map_plot


if __name__ == "__main__":
        import doctest
        doctest.testmod()
