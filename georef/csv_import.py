class NumberOfColumnsException(Exception):
    pass


class EmptyFileException(Exception):
    pass


def check_file_structure(file_array):
    if len(file_array) < 2:
        raise EmptyFileException()
    numlinia = 1
    for rows in file_array:
        if len(rows) != 16:
            raise NumberOfColumnsException({"numrow": str(numlinia), "numcols": str(len(rows))})
        numlinia = numlinia + 1