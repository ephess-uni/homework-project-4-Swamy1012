# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    
    x = [datetime.strptime(od, "%Y-%m-%d").strftime('%d %b %Y') for od in old_dates]
    
    return x

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        
        raise TypeError()
    
    rt = []
    
    a = datetime.strptime(start, '%Y-%m-%d')
    
    for i in range(n):
        
        rt.append(a + timedelta(days=i))
        
    return rt


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    
    adr = date_range(start_date, len(values))
    adrq = list(zip(adr, values))
    return adrq

def fees_report(infile, outfile):
    
    headers = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    
    datawithfees = defaultdict(float)
    
    with open(infile, 'r') as fl:
        linesData = DictReader(fl, fieldnames=headers)
        rows = [row for row in linesData]

    rows.pop(0)
       
    for each_line in rows:
       
        patronID = each_line['patron_id']
        date_due = datetime.strptime(each_line['date_due'], "%m/%d/%Y")
        date_returned_on = datetime.strptime(each_line['date_returned'], "%m/%d/%Y")
        dsdrf = (date_returned_on - date_due).days
        datawithfees[patronID]+= 0.25 * dsdrf if dsdrf > 0 else 0.0
        
            
    rt1 = [
        {'patron_id': pn, 'late_fees': f'{fs:0.2f}'} for pn, fs in datawithfees.items()
    ]
    with open(outfile, 'w') as fl:
        
        wtr = DictWriter(fl,['patron_id', 'late_fees'])
        wtr.writeheader()
        wtr.writerows(rt1)

# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    #BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    #BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report('book_returns.csv', OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
