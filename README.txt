===========
xsvlib
===========

A lightweight library for manipulating CSV files in Python. It requires much less boilerplate code
than the built-in `csv` module, has a smaller memory footprint than `pandas`, and is easier to use
than `fastcsv`.

usage
=========

    from xsvlib import XSV
    xsv = XSV("example.csv")
    xsv.add_column("summation", lambda row: sum(map(int, row)))
    xsv.remove_column(1)
    xsv.rename_column(1, "b")
    xsv.reorder_column([2, 0, 1])
    xsv.map_column(1, int)
    for row in xsv.rows():
        print(row) # print all of the rows!
    xsv.save("example.new.csv")
