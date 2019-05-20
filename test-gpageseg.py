import os
import subprocess
import argparse

mptv_default = os.path.join(os.getenv("HOME"),"Git/OCR4All/mptv/")

def test(source_project, mptv=mptv_default):
    command = "python2 {} --maxcolseps -1 --parallel 8 --nocheck --minscale 12 --maxlines 300 --scale 0 --hscale 1 --vscale 1 --threshold 0.2 --noise 8 --maxseps 2 --sepwiden 10 --csminheight 10 --csminaspect 0.1 --pad 3 --expand 3".format(os.path.join(mptv,"ocropus-gpageseg")).split(" ")

    for image in os.listdir(source_project):
        image_dir = os.path.join(source_project,image)
        if os.path.isdir(image_dir):
            for section in os.listdir(image_dir):
                if section.endswith(".png") and section.count(".") == 1:
                    section_path = os.path.join(image_dir,section)
                    command.append(section_path)

    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''
''')
    parser.add_argument('INPUT', type=str, help='Source input dir to process')
    parser.add_argument('--mptv', type=str, default=mptv_default, help='MPTV folder')
    args = parser.parse_args()

    test(args.INPUT,args.mptv)
