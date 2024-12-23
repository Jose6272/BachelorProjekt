from xml.etree import ElementTree as ET 
import re
import glob 
import argparse
import glob
import os

parser = argparse.ArgumentParser(description="Process input and output directories.")
parser.add_argument('-i', '--input-dir', required=True, help="Path to the input directory")
parser.add_argument('-o', '--output-dir', required=True, help="Path to the output directory")

args = parser.parse_args()

if not os.path.isdir(args.input_dir):
    raise NotADirectoryError(f"Input directory does not exist: {args.input_dir}")
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir, exist_ok=True)

os.chdir(args.input_dir)

def Autosavefiles_parser(filepath):
    liste = []
    for file in glob.glob("**\\AutoSaved*.ps1", recursive=True):
        with open(file, "r") as autofile:
            # læs filens indhold som tekst
            content = autofile.read()
            # gem det hele i listen
            liste.append(content)
    return liste
                
def writeoutput(outputpath, liste):
    with open(outputpath + "\\Autosavefiledata.txt", "w") as Auto:
        for stuff in liste:
            Auto.write(f"{stuff}\n")
Autosaveoutput = Autosavefiles_parser(args.input_dir)
writeoutput(args.output_dir, Autosaveoutput)               
