from FileClass import *

ROOT_PATH  = ""
current_path = ROOT_PATH
current_file = None

#print(len(data["0"]))

######################      Function that operate on/modify File structure    ################

def create(command_full):
        
        try:
            file_path      = command_full.split()[1]
            file_path      = getAbsPathfromRelPath(file_path)
           
            file_to_create = file_path.split("/")[-1]
            parent_dir     = file_path.split("/")[:-1]
            hierarchy      = checkHierarchy(parent_dir)

            if type(hierarchy) == str:
                print(f"\nERROR: Directory '{hierarchy}' could not be found")
            else:
                try:
                    #Checking if the File already exists
                    hierarchy[file_to_create]
                    print(f"ERROR: File '{file_path}' already exists")

                except KeyError as ke:
                    hierarchy[file_to_create] = {
                                                    "type"     : "file",
                                                    "extension": ".txt",
                                                    "data"     : {}
                                                }

                    with open("structure.json", "w") as f:
                        json.dump(structure, f)

                    print(f"File '{file_path}.txt' created")

        except IndexError as ie:
                print("\nERROR: No File name or path specified, usage: 'Create <filePath>'")


def delete(command_full):

        try:
            file_path      = command_full.split()[1]
            file_path      = getAbsPathfromRelPath(file_path)
            file_to_delete = file_path.split("/")[-1]
            parent_dir     = file_path.split("/")[:-1]
            hierarchy      = checkHierarchy(parent_dir)

            #print("PATH: ", file_path)
            if type(hierarchy) == str:
                print(f"\nERROR: Directory '{hierarchy}' could not be found")
            else:
                try:
                    #Checking if the File exists
                    hierarchy[file_to_delete]
                    
                    if hierarchy[file_to_delete]["type"] != "file":
                        print(f"'{file_path}' is not a file")

                    else:
                        hierarchy.pop(file_to_delete)

                        with open("structure.json", "w") as f:
                            json.dump(structure, f)

                        print(f"File '{file_path}.txt' DELETED")

                except KeyError as ke:
                    #If the file does not Exist
                    print(f"File {file_path}.txt does not exist")

        except IndexError as ie:
                print("\nERROR: No Directory name or path specified, usage: 'Delete <filePath>'")


def mkDir(command_full):
       
    try:
        dir_path = command_full.split()[1]
        dir_path = getAbsPathfromRelPath(dir_path)
        
        dir_to_create = dir_path.split("/")[-1]
        parent_dir = dir_path.split("/")[:-1]
        
        hierarchy = checkHierarchy(parent_dir)
       
        if type(hierarchy) == str:
            print(f"\nERROR: Directory '{hierarchy}' could not be found")
        else:
            #MAKE THE DIR IN STRUCTURE LOGIC
            try:
                #Checking if the Directorry already exists
                hierarchy[dir_to_create]
                print(f"ERROR: Directory '{dir_path}' already exists")
            except KeyError as ke:

                #Adding the directory to Parent Directory
                hierarchy[dir_to_create] = {"type": "dir"}

                #print(structure)
                with open("structure.json", "w") as f:                  
                    json.dump(structure, f)

                print(f"Directory '{dir_path}' Created")

    except IndexError as ie:
        print("\nERROR: No Directory name or path specified, usage: 'MkDir <directoryPath>'")
       

def chDir(command_full):

    global current_path
        
    try:
        dir_path = command_full.split()[1]

        if dir_path == "..":
            dir_path = getParent(current_path)
        else:
            dir_path = getAbsPathfromRelPath(dir_path)

        
        #Logic For moving upward in the File Structure to root
        if dir_path == ROOT_PATH:            
            if current_path == ROOT_PATH:
                print(f"Already in root")
                return
            else:

                current_path = ROOT_PATH
                print(f"Setting current path to root")
                return

        #Logic For moving upward or downward in the FIle Structure according to the user input
        hierarchy = checkHierarchy(dir_path.split("/"))
        
        if type(hierarchy) == str:
            print(f"\nERROR: Directory '{hierarchy}' could not be found")
            
        else:

            if hierarchy["type"] != "dir":
                print(f"ERROR: {dir_path} is not a directory")

            else:
                print(f"Setting current path to '{dir_path}'")
                current_path = dir_path 

    #Dispaying Error msg incase of incorrect use of command line
    except IndexError as ie:
        print("\nERROR: No Directory name or path specified, usage: 'ChDir <directoryPath>'")


def showMap():

    global current_path
    
    current_dict = getDictFromPath(current_path)
    prettyPrint(current_dict, 1)


def move(command_full):

    try:
        src_file_path  = command_full.split()[1]
        src_file_path = getAbsPathfromRelPath(src_file_path)
        src_filename   = src_file_path.split("/")[-1]

        trgt_file_path = command_full.split()[2]
        trgt_file_path = getAbsPathfromRelPath(trgt_file_path)
        trgt_filename  = trgt_file_path.split("/")[-1]

        #print(src_file_path, trgt_file_path)
        #print(src_filename, trgt_filename)
        src_hierarchy  = checkHierarchy(src_file_path.split("/"))
        trgt_hierarchy = checkHierarchy(trgt_file_path.split("/"))

        #Checking if both files exist
        if type(src_hierarchy) == str:
            print(f"\nERROR: Source File '{src_hierarchy}'.txt could not be found")
            return
        if type(trgt_hierarchy) == str:
            print(f"\nERROR: Source File '{trgt_hierarchy}'.txt could not be found")
            return
        
        #Reading the data from the Source File
        src_file_obj = CustomFile(src_filename, src_hierarchy, "r")
        src_data     = src_file_obj.read()

        #Writing the data from the Source File
        trgt_file_obj = CustomFile(trgt_filename, trgt_hierarchy, "w") ###Either w or a
        trgt_file_obj.write(src_data)

        print(src_file_obj)
        print(trgt_file_obj)


    except IndexError as ie:
        print("\nERROR: No Directory name or path specified, usage: 'ChDir <directoryPath>'")    


######################    Functions that operate on/modify File Data    ######################

def Open(command_full):
    
    global current_file

    if current_file:
        print(f"ERROR: A file {current_file.name}.txt is already opened, Please close it using the 'Close' command before opening another")
        return

    try:
        file_path      = command_full.split()[1]
        file_mode      = command_full.split()[2]

        if file_mode not in ["r", "rf", "t", "a", "w"]:
            print(f"ERROR: Invalid mode, Please chose a mode from: 'r', 't', 'a', 'w'")
            return

        file_path      = getAbsPathfromRelPath(file_path)
        
        file_name   = file_path.split("/")[-1]

        #hierarchy is the required file json object
        hierarchy      = checkHierarchy(file_path.split("/"))

        if type(hierarchy) == str:
            print(f"File '{file_path}'.txt does not exist")

        else:

            if hierarchy["type"] != "file":
                print(f"'{file_path}' is not a file")

            else:
                current_file = CustomFile(file_name, hierarchy, file_mode)   
                print(f"'{file_path}.txt' succesfully Opened in '{file_mode}' mode")   
               

    except IndexError as ie:
        print("\nERROR: Invalid use of Open command, usage: 'Open <filename> <mode>'")


def close(command_full):

    """
    This is the function that is called for the 'Close' command.
    It sets the current_file global variable to None if it is not None

    @param command_full: The full command form the command line
    """

    global current_file

    if not current_file:
        print(f"ERROR: No file is opened, Please open a file using 'Open <filename> <mode>' before using 'Close' command")
        return
    
    print(f"{current_file.name}.txt succesfully Closed")
    current_file = None


def read():

    global current_file

    if not current_file:
        print(f"ERROR: No file is opened, Please open a file using 'Open <filename> <mode>' before using 'Read' command")
        return

    read_data = current_file.read()
    if read_data:
        print(read_data)


def readFrom(command_full):

    global current_file

    try:

        start_index = int(command_full.split()[1])
        size        = int(command_full.split()[2])

        if not current_file:
            print(f"ERROR: No file is opened, Please open a file using 'Open <filename> <mode> before using 'ReadFrom' command")
            return

        # perform read operation
        read_data = current_file.readFrom(data, start_index, size)

        if read_data:
            print(read_data)

    except IndexError as e:
        print("\nERROR: Invalid use of ReadFrom command, usage: 'ReadFrom <index> <size>'")



def append():

    if not current_file:
        print(f"ERROR: No file is opened, Please open a file using 'Open <filename> <mode> before using 'Append' command")
        return

    try:
        text_to_append = input("\nEnter text to append : \n")
        # append text to file
        current_file.append(text_to_append, data)
        
        #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)

    except IndexError as ie:
        print("\nERROR: Invalid use of Append command, usage: 'Append'")


def truncate(command_full):

    if not current_file:
        print(f"ERROR: No file is opened, Please open a file using 'Open <filename> <mode> before using 'ReadFrom' command")
        return

    try:
        size = int(command_full.split()[1])

        current_file.truncate(data, size)
        
        #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)

    except IndexError as ie:
        print("\nERROR: Invalid use of Truncate command, usage: 'Truncate <size>'")



def write():

    if not current_file:
        print(f"ERROR: No file is opened, Please open a file using 'Open <filename> <mode> before using 'Write' command")
        return

    text = input("Text : \n")
    current_file.write(text)

    #Updating the File Structure and Data Storage in Non-Volatile memory
    with open("structure.json", "w") as f:
        json.dump(structure, f)


def writeAt(command_full):

    if not current_file:
        print(f"ERROR: No file is opened, Please open a file using 'Open <filename> <mode> before using 'Write' command")
        return

    try:
        index = int(command_full.split()[1])

        text = input("\nText : \n")
        current_file.writeAt(data, text, index)
        #print(len(data["0"]))

        #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)

    except IndexError as ie:
        print("\nERROR: Invalid use of WriteAt command, usage: 'Truncate <index>'")



def move_within_file(command_full):

    

    if not current_file:
        print(f"ERROR: No file is opened, Please open a file using 'Open <filename> <mode> before using 'Move' command")
        return

    try:
        start_index = int(command_full.split()[1])
        to = int(command_full.split()[2])
        size = int(command_full.split()[3])

        current_file.move(start_index, to, size)


         #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)

    except IndexError as ie:
        print("\nERROR: Invalid use of MoveWithin command, usage: 'MoveText <from> <to> <size>'")


######################    Utility Functions    ###############################################

def checkHierarchy(path):

    """
    A Function tat checks the validity of a path in the file structure
    If the argument 'path' is valid, the function returns a dictionary Object of the file/dir,
    else returns a String that specifies the invalid path

    @param path: a list all the directoires in the hierarchy
    """

    dir_str  = ""
    dir_dict = getDictFromPath(dir_str)
    
    for idx, dir_name in enumerate(path):
        
        if path[idx] in dir_dict.keys():
            
            if dir_str == "":
                dir_str +=  path[idx]
            else:
                dir_str += "/" + path[idx]
            
            dir_dict = getDictFromPath(dir_str)
            
        else:
            #Returning invalid path string
            return dir_str + "/" + path[idx]

    #Returning Directory dictionary object
    return dir_dict

def getDictFromPath(dir_path):

    """   
    A fucntion that returns dictionary object of directory

    @param dir_path: The path of the directory
    """

    temp = root

    if not dir_path:
        return temp
    
    found_dir_hierarchy = dir_path.split("/")
    for i in found_dir_hierarchy:
        temp = temp[i]

    return temp

def prettyPrint(d, indent=0):

    """
    A function used to pretty print the file structure

    @param d:      A dict object to pretty print
    @param indent: The indent from which to start printing, defaults to 0
    """

    for key, value in d.items():

        if key not in ["type", "extension", "data", "page"]:
            
            if isinstance(value, dict):
                print('  ' * indent + str(key) + ": " + str(value["type"]))
                prettyPrint(value, indent+1)
            else:
                print('  ' * (indent+1) + str(value))

def getAbsPathfromRelPath(rel_path):

    """
    A function that takes in a relative path 
    and returns the absolute path i.e from the root

    @param rel_path: The path relative to the current path
    """

    global current_path

    if current_path:
        return current_path + "/" + rel_path
        
    return rel_path

def getParent(path):

    """
    A Function that returns the parent directory's path of a given directory/file.
    Returns ROOT_PATH is path is ROOT_PATH, else returns the parent.

    @param path: A String of the path of directory or file 
    """

    if path == ROOT_PATH:
        return ROOT_PATH

    path_list = path.split("/")[:-1]

    if len(path_list):
        print("/".join(path_list))
        return "/".join(path_list)

    return ROOT_PATH


