import pandas as pd
from bokeh.palettes import Greys256
from bkcharts import Bar, show, defaults, cat

def makeStackedBar(df, x, y, sort_x=False, x_ascending=True, sort_bars=False, bars_col='', bars_agg=None, bars_ascending=True, 
                sort_stacks=False, stacks_col='', stacks_agg=None, stacks_ascending=True, colors=Greys256, title="title"):
    '''
    Parameters
    ----------
    df : str
        Dataframe containing data
    x : str
        Column name for x-axis
    y : str
        Column name for y-axis
    sort_x : boolean
        Boolean whether to sort by x-axis
    x_ascending : boolean
        Boolean to sort x's by ascending
    sort_bars : boolean
        Boolean whether to sort bars
    bars_col : str
        Column name of values of bars 
    bars_agg : function
        Function to apply to aggregation to sort bars by
    bars_ascending : boolean
        Boolean to sort bars ascending
    sort_stacks : boolean
        Boolean whether to sort stacks
    stacks_col : str
        Column name of values for stacks 
    stacks_agg : function
        Function to apply to aggregation to sort stacks by
    stacks_ascending : boolean
        Boolean to sort bars ascending
    colors : color palette
        Pass in a Bokeh color palette

    Returns
    -------
    Returns a stacked bar chart object of x by y. The bars and stacks can be
    generated by the passed in aggregation function or directly passed in. The
    sorting will prioritize bars before the x-axis values.
    '''
    if bars_agg:
        bar = df.groupby([x, y]).apply(bars_agg).reset_index()
    elif bars_col:
        bar = df[[x, y, bars_col]]
    else:
        bar = df.groupby([x, y]).size().reset_index()

    bar.columns = [x, y, 'bar_order']
    if stacks_agg:
        bar['stack_order'] = (bar.groupby(x)['bar_order']
                                            .transform(stacks_agg))
    elif stacks_col:
        bar['stack_order'] = df[stacks_col]
    else:
        raise ValueError('No values for stacks')

    sort = []
    ascend = []
    if sort_stacks:
        sort.append('stack_order')
        ascend.append(bars_ascending)
    if sort_bars:
        sort.append('bar_order')
        ascend.append(stacks_ascending)
    if sort_x:
        sort.append(x)
        ascend.append(x_ascending)
    bar = bar.loc[bar.sort_values(sort, ascending=ascend).index]
    unique_vals = bar[y].unique().size

    bar_plot = Bar(bar, label=cat(columns=x, sort=False), 
                    palette=colors(unique_vals), values='bar_order', 
                    stack=y, responsive=True, active_scroll='wheel_zoom',
                    title=title)

    return bar_plot


if __name__ == "__main__":
        import doctest
        doctest.testmod()
