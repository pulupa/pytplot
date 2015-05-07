def applySmartTimeTicks(ax, time, dolimit = True):
    """
    Given an axis 'ax' and a list/array of datetime objects, 'time',
    use the smartTimeTicks function to build smart time ticks and
    then immediately apply them to the given axis.  The first and
    last elements of the time list will be used as bounds for the
    x-axis range.

    The range of the 'time' input value will be used to set the limits
    of the x-axis as well.  Set kwarg 'dolimit' to False to override
    this behavior.

    Parameters
    ==========
    ax : matplotlib.pyplot.Axes
        A matplotlib Axis object.
    time : list
        list of datetime objects
    dolimit : boolean (optional)
        The range of the 'time' input value will be used to set the limits
        of the x-axis as well. Setting this overrides this behavior.

    See Also
    ========
    smartTimeTicks
    """
    Mtick, mtick, fmt = smartTimeTicks(time)
    ax.xaxis.set_major_locator(Mtick)
    ax.xaxis.set_minor_locator(mtick)
    ax.xaxis.set_major_formatter(fmt)
    if dolimit:
        ax.set_xlim([time[0], time[-1]])
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_horizontalalignment('center')
        tick.label1.set_rotation(0)

def smartTimeTicks(time):
    """
    Returns major ticks, minor ticks and format for time-based plots

    smartTimeTicks takes a list of datetime objects and uses the range
    to calculate the best tick spacing and format.  Returned to the user
    is a tuple containing the major tick locator, minor tick locator, and
    a format string -- all necessary to apply the ticks to an axis.

    It is suggested that, unless the user explicitly needs this info,
    to use the convenience function applySmartTimeTicks to place the
    ticks directly on a given axis.

    Parameters
    ==========
    time : list
        list of datetime objects

    Returns
    =======
    out : tuple
        tuple of Mtick - major ticks, mtick - minor ticks, fmt - format

    See Also
    ========
    applySmartTimeTicks
    """
    from matplotlib.dates import (MinuteLocator, HourLocator, MonthLocator,
                                  DayLocator, DateFormatter,drange)
    from matplotlib.ticker import FixedLocator
    from matplotlib import rcParams
    import datetime

    deltaT = time[-1] - time[0]
    nHours = deltaT.days * 24.0 + deltaT.seconds/3600.0
    if nHours > 48:
        firsttick=time[0]
        if firsttick != datetime.datetime.combine(firsttick.date(),datetime.time()):
            firsttick = firsttick + datetime.timedelta(1)
            print(firsttick)
    if nHours < 1:
        Mtick = MinuteLocator(byminute = [0,15,30,45])
        mtick = Mtick # MinuteLocator(byminute = list(range(60)), interval = 5)
        if rcParams['text.usetex']:
            fmt = DateFormatter('$%H%M$')
        else:
            fmt = DateFormatter('%H%M')
    elif nHours < 4:
        Mtick = MinuteLocator(byminute = [0,30])
        mtick = MinuteLocator(byminute = list(range(60)), interval = 10)
        if rcParams['text.usetex']:
            fmt = DateFormatter('$%H%M$')
        else:
            fmt = DateFormatter('%H%M')
    elif nHours < 12:
        Mtick = HourLocator(byhour = list(range(24)), interval = 2)
        mtick = MinuteLocator(byminute = [0,15,30,45])
        if rcParams['text.usetex']:
            fmt = DateFormatter('$%H%M$')
        else:
            fmt = DateFormatter('%H%M')
    elif nHours < 24:
        Mtick = HourLocator(byhour = [0,3,6,9,12,15,18,21])
        mtick = HourLocator(byhour = list(range(24)))
        if rcParams['text.usetex']:
            fmt = DateFormatter('$%H%M$')
        else:
            fmt = DateFormatter('%H%M')
    elif nHours < 48:
        Mtick = HourLocator(byhour = [0,6,12,18])
        mtick = HourLocator(byhour = list(range(24)))
        if rcParams['text.usetex']:
            fmt = DateFormatter('$%H%M$')
        else:
            fmt = DateFormatter('%H%M')
    elif nHours < 24 * 7:
        Mtick = DayLocator(bymonthday = list(range(1,32)))
        mtick = HourLocator(byhour = [0,6,12,18])
        if rcParams['text.usetex']:
            fmt = DateFormatter('$%d %b$')
        else:
            fmt = DateFormatter('%d %b')
    elif nHours < 24 * 14:
        Mtick = FixedLocator(drange(firsttick.date(),time[-1].date(),datetime.timedelta(days=2)))
        mtick = HourLocator(byhour = [0,12])
        if rcParams['text.usetex']:
            fmt = DateFormatter('$%d %b$')
        else:
            fmt = DateFormatter('%d %b')
    elif nHours < 24 * 30:
        Mtick = FixedLocator(drange(firsttick.date(),time[-1].date(),datetime.timedelta(days=4)))
        mtick = HourLocator(byhour = [0])
        if rcParams['text.usetex']:
            fmt = DateFormatter('$%d %b$')
        else:
            fmt = DateFormatter('%d %b')
    elif nHours < 24 * 60:
        Mtick = FixedLocator(drange(firsttick.date(),time[-1].date(),datetime.timedelta(days=10)))
        mtick = HourLocator(byhour = [0])
        if rcParams['text.usetex']:
            fmt = DateFormatter('$%d %b$')
        else:
            fmt = DateFormatter('%d %b')
    else:
        Mtick = MonthLocator()
        mtick = MonthLocator()
        if rcParams['text.usetex']:
            fmt = DateFormatter('$%b %y$')
        else:
            fmt = DateFormatter('%b %y')

    return (Mtick, mtick, fmt)
'''
Created on Jul 13, 2013

@author: pulupa
'''
