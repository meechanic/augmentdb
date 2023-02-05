import sys
import csv
from io import StringIO


def sepval_load(f, with_header=None, delimiter=None, header=None, type=None):
    ret = None
    if delimiter == None:
        delimiter = "|"
    if type == None or type == "list":
        ret = []
        if with_header:
            reader = csv.DictReader(f, delimiter=delimiter)
            for i in reader:
                ret.append(i)
        else:
            if header != None:
                reader = csv.DictReader(f, delimiter=delimiter, fieldnames=header)
                for i in reader:
                    ret.append(i)
            else:
                reader = csv.reader(f, delimiter=delimiter)
                for i in reader:
                    ret.append({j: i[j] for j in range(0, len(i))})
    elif type == "object":
        ret = {}
        reader = csv.DictReader(f, delimiter=delimiter, fieldnames=["key", "value"])
        for i in reader:
            ret[i["key"]] = i["value"] 
    elif type == "single":
        ret = f.read()
    else:
        sys.stderr.write("Unknown type: {}\n".format(type))
        exit(1)
    return ret


def sepval_dump(data, f, delimiter=None, no_header=None, no_data=None):
    if delimiter == None:
        delimiter = "|"
    if isinstance(data, list):
        writer = csv.DictWriter(sys.stdout, delimiter=delimiter, fieldnames = data[0].keys(), extrasaction='ignore')
        if not no_header:
            writer.writeheader()
        if not no_data:
            for row in data:
                writer.writerow(row)
    elif isinstance(data, dict):
        if not no_header:
            f.write("key" + delimiter + "value\n")
        for k in data:
            f.write(k + delimiter + str(data[k]) + "\n")
    else:
        f.write(data)
