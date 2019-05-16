import os
import argparse
from shutil import copyfile
import math

def rename(path,orig,replace):          
    return os.path.sep.join([p.replace(orig,replace,1) if p.startswith(orig) else p for p in path.split(os.path.sep)])

def tree(root):
    # Create processing tree
    tree = {}
    for root,dirs,files in os.walk(processing_dir):
        path = os.path.split(root)
        
        current = tree

        for p in path:
            p = p.replace("./","")
            if p not in ["","."]: 
                if p not in current:
                    current[p] = {} 
                current = current[p]
        for directory in dirs:      
            if directory not in current:
                current[directory] = {} 
        current["/files"] = files   
    return tree

def recursive_copy(input_dir,output_dir,orig,replace):
    for content in os.listdir(input_dir):
        current = os.path.join(input_dir,content)
        if content.startswith(orig):
            current_out = os.path.join(output_dir,content.replace(orig,replace,1))
            if os.path.isdir(current):
                if not os.path.exists(current_out):
                    os.makedirs(current_out)
                recursive_copy(current,current_out,orig,replace)
            else:
                copyfile(current,current_out)

def multiply(project_dir,output,count):
    input_dir = os.path.join(project_dir,"input")
    processing_dir = os.path.join(project_dir,"processing")
    images = [os.path.splitext(image) for image in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir,image))]

    # Create base folders in out
    input_dir_out = os.path.join(output,"input")
    processing_dir_out = os.path.join(output,"processing")
    result_dir_out = os.path.join(output,"result")
    if not os.path.exists(input_dir_out):
        os.mkdir(input_dir_out)
    if not os.path.exists(processing_dir_out):
        os.mkdir(processing_dir_out)
    if not os.path.exists(result_dir_out):
        os.mkdir(result_dir_out)

    index = 0
    count_perimage = math.ceil(count/len(images))
    tree = tree(os.path.join(processing_dir))
    for image,ext in images:
        for i in range(count_perimage):
            # Get base name for new image
            index += 1
            name = "{:03d}".format(index)
            # Copy orig
            copyfile(os.path.join(input_dir,image+ext),os.path.join(input_dir_out,name+ext))
            # Copy processed files
            recursive_copy(processing_dir,processing_dir_out,image,name)

            
        





parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))
