import os
import argparse
from shutil import copyfile
import math
from tqdm import tqdm

# Rename a complete folder path.
# Replaces the names of every folder starting with orig, into replace.
def rename(path,orig,replace):          
    return os.path.sep.join([p.replace(orig,replace,1) if p.startswith(orig) else p for p in path.split(os.path.sep)])

# Recursively copy every file and folder starting with orig.
# Replace orig with replace for every copy
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

# Multiply the contents of a source ocr4all project into a new project
# The new project will have count many images, which are multiples of the source project.
def multiply(project_dir,output,count):
    input_dir = os.path.join(project_dir,"input")
    processing_dir = os.path.join(project_dir,"processing")
    result_dir = os.path.join(project_dir,"results")
    images = [os.path.splitext(image) for image in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir,image))]

    # Create base folders in out
    input_dir_out = os.path.join(output,"input")
    processing_dir_out = os.path.join(output,"processing")
    result_dir_out = os.path.join(output,"results")
    if not os.path.exists(input_dir_out):
        os.makedirs(input_dir_out)
    if not os.path.exists(processing_dir_out):
        os.makedirs(processing_dir_out)
    if not os.path.exists(result_dir_out):
        os.makedirs(result_dir_out)

    index = 0
    count_perimage = math.ceil(count/len(images))
    for i in tqdm(range(count_perimage)):
        for image,ext in images:
            if index < count:
                # Get base name for new image
                index += 1
                name = "{:04d}".format(index)
                # Copy orig
                if os.path.exists(input_dir):
                    copyfile(os.path.join(input_dir,image+ext),os.path.join(input_dir_out,name+ext))
                
                # Copy processed files
                if os.path.exists(processing_dir):
                    recursive_copy(processing_dir,processing_dir_out,image,name)
                
                # Copy result files
                if os.path.exists(result_dir):
                    for f in os.listdir(result_dir):
                        f_in = os.path.join(result_dir,f)
                        if os.path.isdir(f_in):
                            f_out = os.path.join(result_dir_out,f)
                            if not os.path.exists(f_out):
                                os.makedirs(f_out)
                            recursive_copy(f_in,f_out,image,name)

            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''
Multiply the contents of a source ocr4all project into a new project.
The new project will have "count" many images, which are copies from images of the source project.''')
    parser.add_argument('INPUT', type=str, help='Source input dir to multiply')
    parser.add_argument('OUTPUT', type=str, help='Output dir to save the multiplied to')
    parser.add_argument('-c','--count', default=10, type=int, help='The maximal number of items that should be added to output (not a multiplier)')

    args = parser.parse_args()

    multiply(args.INPUT,args.OUTPUT,args.count)
