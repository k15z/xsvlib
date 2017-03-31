"""
xsv = XSV("example.csv", delimiter=",", has_header=True)
"""
import csv
from tqdm import tqdm

def write_xsv(filename, rows, encoding="utf8", delimiter=","):
    with open(filename, "wt", encoding=encoding) as fout:
        writer = csv.writer(fout, delimiter=delimiter)
        writer.writerows(tqdm(rows, filename))

class XSV:

    def __init__(self, filename, encoding="utf8", has_header="unknown"):
        self._funcs = []
        self._filename = filename
        self._encoding = encoding
        self._has_header = has_header

        self._fin = open(filename, "rt", encoding=encoding)
        preview = self._fin.read(1024)
        self._fin.seek(0)

        sniffer = csv.Sniffer()
        self._dialect = sniffer.sniff(preview)
        if self._has_header == "unknown":
            self._has_header = sniffer.has_header(preview)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._fin.close()

    def _apply(self, row, is_header=False):
        for func in self._funcs:
            row = func(row, is_header)
        return row

    def rows(self):
        self._fin.seek(0)
        reader = csv.reader(self._fin, self._dialect)
        yield self._apply(next(reader), self._has_header)
        for row in reader:
            yield self._apply(row)

    def save(self, filename):
        with open(filename, "wt", encoding=self._encoding) as fout:
            writer = csv.writer(fout, dialect=self._dialect)
            writer.writerows(tqdm(self.rows(), filename))

    def preview(self):
        return next(self.rows())

    def add_column(self, name, func):
        def my_func(row, is_header):
            return row + [name if is_header else func(row)]
        self._funcs.append(my_func)

    def map_column(self, i, func):
        def my_func(row, is_header):
            if not is_header:
                row[i] = func(row[i])
            return row
        self._funcs.append(my_func)

    def remove_column(self, i):
        def my_func(row, is_header):
            ix = i
            while ix < 0: ix += len(row)
            return row[:ix] + row[ix+1:]
        self._funcs.append(my_func)

    def rename_column(self, i, name):
        def my_func(row, is_header):
            if is_header:
                row[i] = name
            return row
        self._funcs.append(my_func)

    def reorder_column(self, ordering):
        def my_func(row, is_header):
            _row = []
            for i in ordering:
                _row.append(row[i])
            return _row
        self._funcs.append(my_func)
