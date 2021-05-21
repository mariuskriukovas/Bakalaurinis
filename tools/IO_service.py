import datetime
import json
from os import walk, remove, makedirs, path
from qiskit.result import Result

import git.Bakalaurinis.tools.mock_circuit as mock


DIR = ".//results//"


def form_file_name(name):
    ct = datetime.datetime.now()
    dat_str = ct.strftime("%Y_%m_%d_%H_%M_%S_%f")
    full_name = f'{dat_str}_{name}.json'
    return full_name


# form_file_name("Labas")


def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__


# lambda o: o.__dict__
def toJSON(obj):
    return json.dumps(obj, default=json_default,
                      sort_keys=True, indent=4)


def create_dir_if_needed(dir_name):
    dir = f'.{DIR}{dir_name}'
    # dir = f'{READ_DIR}{dir_name}'
    is_exist = path.exists(dir)
    if not is_exist:
        makedirs(dir)
    return is_exist


# create_dir_if_needed("test")

def write_results(result, dir_name, file_name):
    while True:
        if create_dir_if_needed(dir_name): break
    file = f'.{DIR}{dir_name}//{form_file_name(file_name)}'
    with open(file, 'w') as outfile:
        try:
            outfile.write(toJSON(result.to_dict()))
            print("wrote", "===>", file_name)
        except Exception as e:
            print(e)
            outfile.write(str(result.to_dict()))
            print("exception")
        outfile.close()


# write_results(mock.get_MOCK_results(), "test2", "test")


def read_results(dir_name, file_name):
    file = f'.{DIR}{dir_name}//{file_name}'
    with open(file) as f:
        data = json.load(f)
        f.close()
        return Result.from_dict(data)


# print(read_results("test", "2021_04_22_16_36_09_421315_test.json"))

def read_filenames(dir_name, key=""):
    files = []
    for (dirpath, dirnames, filenames) in walk(f'.{DIR}{dir_name}'):
        files.extend(filenames)
        files.extend(dirnames)
        break
    res = []
    if key is not "":
        for f in files:
            if key in f:
                res.append(f)
    else:
        res = files
    return res


# print(read_filenames("x_gate_ibmq_quito", "json"))


def delete_files(dir_name, key):
    file_names = read_filenames(dir_name, key)
    for f in file_names:
        print("removed", "=>", f'.{DIR}{dir_name}//{f}')
        remove(f'.{DIR}{dir_name}//{f}')
    print('done')

# delete_files("test","deleteMe.json")
