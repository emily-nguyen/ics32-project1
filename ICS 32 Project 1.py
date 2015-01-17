# ICS 32 Project #1: Begin the Begin

'''Program that takes in 3 lines of input: (1) directory, (2) search characteristic,
(3) action to perform on file. Uses recursion to look for files in subdirectories and 
filters files by specific criteria'''


import os
import pathlib
import shutil


def check_directory()->pathlib.Path:
    '''Get first line of input and checks if directory path is valid; returns path
    else prints ERROR'''

    while True: 
        root_dir = input().strip()
        path = pathlib.Path(root_dir) 

        if path.is_dir() and path.exists():
            return path
        print('ERROR')


def path_list(lst: list)->list:
    '''Takes a list of names of entries in the directory and returns a list of their
    paths'''

    result = [] 

    for i in lst:
        x = os.path.realpath(i)
        result.append(x)
    return result


def is_num(value: str)->bool:
    '''Returns True if string can be converted to number, return False otherwise'''

    try:
        value = int(value)
        return True
    except:
        return False 


def search_parameters(path: str)->list:
    '''Get second line of input and performs specified search; returns list of paths
    with characteristics; else prints ERROR'''

    os.chdir(path)
    lst = os.listdir(path)
    start_list = path_list(lst)
    value, new_list, result = '', [], []

    while True:
        try: 
            input_list = input().strip().split()
            search_type = input_list[0]
            names, value = input_list[1:], input_list[1]
        except:
            pass

        length = len(input_list)
        master = master_list(start_list, result)

        if search_type == 'N' and length >= 2: 
            return search_name(names, master, new_list)
        elif search_type == 'E' and length == 2:
            return search_extension(value, master, new_list) 
        elif search_type == 'S' and length == 2:
            if is_num(value): 
                return search_size(int(value), new_list)
            print('ERROR')
        else:
            print('ERROR')


def add_change(item: str, result: list)->None:
    '''Changes the directory, add file paths to list of paths, and changes back to
    parent directory'''
   
    os.chdir(item)
    lst = os.listdir(item)
    for i in lst:
        result.append(os.path.realpath(i))
    os.chdir('.')


def master_list(start_list: list, result: list)->list:
    '''Performs recursion to return a master list of files in a given directory'''

    if start_list == []:
        return result
    else:
        item = start_list[0]

        if os.path.isfile(item):
            result.append(item)
            return master_list(start_list[1:], result)
        elif os.path.isdir(item):
            add_change(item, result)
            return master_list(start_list[1:], result)
        else:
            print('ERROR')
    

def search_name(name_list: list, result: list, new_list: list)->list:
    '''Searches if files match those in the name list; return list of matching files;
    else prints ERROR'''

    for item in result:
        basename = os.path.basename(item)
        
        if basename in name_list: 
            new_list.append(item)
    return new_list



def search_extension(ending: str, result: list, new_list: list)->list:
    '''Searches if files match extension specified; returns list of matching files;
    else prints ERROR'''

    for item in result:
        basename = os.path.basename(item)
        
        if basename.endswith(ending):
            new_list.append(item)
    return new_list


def search_size(size: int, new_list: list)->list:
    '''Searches if files' sizes are greater than size specified; returns list of matching
    files; else prints ERROR'''
        
    if os.path.getsize(item) > size:
        new_list.append(item)
    return new_list


def open_file(filename: str):
    '''Tries to read and print first line in file; closes file afterwards'''

    try: 
        infile = open(filename)
        first_line = infile.readline()
        print(first_line)
    finally: 
        infile.close()


def copy_file(filename: str):
    '''Copies the file and creates a new file with same name and added .dup extension'''

    shutil.copyfile(filename, filename + '.dup')


def touch_file(filename: str):
    '''Changes the timestamp of file to current time'''

    os.utime(filename)


def template(result: list, f: 'function'):
    '''Template function that prints each item in list, and calls the action on the item'''

    for i in result:
        print(i)
        f(i)


def perform_action(result: list):
    '''Get third line of input and performs specified action, else prints ERROR'''

    while True:
        ch = input().strip()

        if ch in 'PFDT':
            if ch == 'P':
                for i in result:
                    print(i)
                break 
            elif ch == 'F':
                template(result, open_file) 
                break
            elif ch == 'D':
                template(result, copy_file)
                break
            elif ch == 'T':
                template(result, touch_file)
                break
        else:
            print('ERROR')

    
def main():
    '''Execute function to search and perform file manipulation'''

    path = str(check_directory())
    result = search_parameters(path)
    perform_action(result) 

    
if __name__ == '__main__':
    main()
