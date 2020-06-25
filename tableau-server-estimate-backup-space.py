import os
import math
import shutil
import ctypes  

#returns a boolean for y/n user input
def get_answer(choice):
    while choice not in ["y", "n"]: 
        choice = input("Please respond with 'y' or 'n': ") 
    if choice == "y":
       return True
    elif choice == "n":
       return False 
       
#returns size (int) of a folder given a filepath
def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp) #size in bytes 
    total_size=math.ceil(total_size/1024/1024)
    print ("Total Size of folder:" + str(total_size) + "MB")     
    return total_size

#returns config of the node 
def get_node_config(r,f,c): 
    nodeConfig=""
    if r: 
        nodeConfig+="r"
    if f:
        nodeConfig+="f"
    if c: 
        nodeConfig+="c"
    return nodeConfig
    
#returns diskspace reqs based on help guide estimate calculations 
def get_required_size(nodeConfig): 
    required_size_est = 0
    if nodeConfig=="r":
        required_size_est = get_repo_size()*3 + 250
    elif nodeConfig=="f":
        required_size_est=get_fs_size()*1.5
    elif nodeConfig=="c" or nodeConfig=="rc":
        required_size_est=get_repo_size()*3 + 250 + (get_fs_size()*2.5)
    elif nodeConfig=="rf" or nodeConfig=="fc" or nodeConfig=="rfc":
        required_size_est=get_repo_size()*3 + 250 + get_fs_size()*1.5
    else: 
        print("This doesn't look right...are your parameters correct?")
    print ("This is the *estimated* diskspace you need for a backup: " + str(required_size_est) + "MB")
    return required_size_est
    
#returns the size of <data directory>/pgsql/data/base 
def get_repo_size(): 
    start_path=input("Please enter the exact filepath for your pgsql base directory. Default is <data directory>/pgsql/data/base directory: ")
    return get_size(start_path)
    
#returns the size of <data directory>/dataengine
def get_fs_size(): 
    start_path=input("Please enter the exact filepath for your dataengine directory. Default is <data directory>/dataengine: ")
    return get_size(start_path)
    
# returns the free space available
def get_free_space(): 
    total, used, free = shutil.disk_usage("/")
    print("This is the total disk space you currently have on this computer: ")
    print("Total: %d GiB" % (total // (2**30)))
    print("Used: %d GiB" % (used // (2**30)))
    print("Free: %d GiB" % (free // (2**30)))
    
def main(): 
    #define r_node, is there a repo? 
    r_node = get_answer(input("Is there a Repository on this node? y/n: ")) 
    #print ("This is r_node: " + str(r_node))
    #define fs_node, is there a filestore? 
    f_node = get_answer(input("Is there a Filestore on this node? y/n: ")) 
    #print ("This is f_node: " + str(f_node))
    #define c_node, is there a controller? 
    c_node = get_answer(input("Is there a Controller on this node? y/n: ")) 
    #print ("This is c_node: " + str(c_node))
    
    nodeConfig = get_node_config(r_node,f_node,c_node)
    get_required_size(nodeConfig)
    get_free_space()
    
    ctypes.windll.user32.MessageBoxW(0, "These results are just an *estimate* - the actual backup size will be slightly larger than this due to temp and config files. This tool is also provided as-is and is not officially supported by Tableau Support.", "Important Note", 1)

main()