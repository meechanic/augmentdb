import os
import sys
import traceback
import pandas as pd
from random import seed, randint
from pathlib import PurePath


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def eprint_exception(e, print_traceback=True, need_exit=True):
    eprint(e)
    if print_traceback:
        eprint(traceback.format_exc())
    if need_exit:
        exit(1)


def filter_by_args(args, item):
    ret = False
    filter_performed = False
    if args.type:
        if args.type == "dir":
            if os.path.isdir(item):
                ret = True
        if args.type == "nondir":
            if not os.path.isdir(item):
                ret = True
        filter_performed = True
    if args.glob:
        ret = ret or PurePath(item).match(args.glob)
        filter_performed = True
    if not filter_performed:
        ret = True
    return ret



def ls(path, args):
    if args.detalization == None or args.detalization == "0" or args.detalization == "names":
        return [{"name": element.name} for element in os.scandir(path) if filter_by_args(args, element.name)]
    else:
        return [{"name": element.name, "atime": element.stat()[7], "mtime": element.stat()[8], "ctime": element.stat()[9]} for element in os.scandir(path) if filter_by_args(args, element.name)]


def pd_obj_transform(obj, keyname):
    ret = []
    for i in obj.keys():
        obj[i][keyname] = i
        ret.append(obj[i])
    return ret


def enrich(input_obj1, input_obj2, key1="name", key2="name", how="outer"):
    inp_df1 = pd.DataFrame(input_obj1).set_index(key1)
    inp_df2 = pd.DataFrame(input_obj2).set_index(key2)
    return pd_obj_transform(inp_df1.merge(inp_df2, left_index=True, right_index=True, how=how).T.to_dict(), key1)


def objmerge(input_obj1, input_obj2):
    for i in input_obj2:
        input_obj1[i] = input_obj2[i]
    return input_obj1


def richdb_get(input_obj, key, value, all):
    ret = None
    if all == True:
        ret = []
        for i in input_obj:
            if i[key] == value:
                ret.append(i)
    else:
        for i in input_obj:
            if i[key] == value:
                ret = i
                break
    return ret


def unique_randint(lower_bound, upper_bound, list_of_integers):
    seed()
    while True:
        new_int = randint(lower_bound, upper_bound)
        if new_int not in list_of_integers:
            return new_int


def enrich_by_ids(input_obj, rewrite):
    seed()
    u = len(input_obj) * 2
    if u < 65536:
        u = 65536
    if rewrite == True:
        all_ids = []
        for i in input_obj:
            i["id"] = unique_randint(0, u, all_ids)
            all_ids.append(i["id"])
    else:
        all_ids = []
        for i in input_obj:
            if "id" in i:
                all_ids.append(i["id"])
        for i in input_obj:
            if "id" not in i:
                i["id"] = unique_randint(0, u, all_ids)
                all_ids.append(i["id"])
    return input_obj
