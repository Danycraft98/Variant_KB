import os
import pandas


def read_file(file, **kwargs):
    """Read file with **kwargs; files supported: xls, xlsx, csv, csv.gz, pkl"""
    read_map = {
        'xls': pandas.read_excel, 'xlsx': pandas.read_excel, 'csv': pandas.read_csv,
        'gz': pandas.read_csv, 'pkl': pandas.read_pickle
    }

    ext = os.path.splitext(file.name)[1].lower()[1:]
    assert ext in read_map, "Input file not in correct format, must be xls, xlsx, csv, csv.gz, pkl; current format '{0}'".format(ext)
    # assert os.path.isfile(file.name), "File Not Found Exception '{0}'.".format(file.name)
    return read_map[ext](file, **kwargs)
