#!/usr/bin/python3
from xml.etree import ElementTree as ET # libary som kan arbejde med xml-filer
import argparse #Libary som håndtere kommandolinje argumenter
import glob #libary som kan finde filer med mønstre
import os # libary til at arbejde med fil og mappe placeringer
import re #libary for brugen af regex mønstre 


parser = argparse.ArgumentParser(description="Process input and output directories.")
parser.add_argument('-i', '--input-dir', required=True, help="Path to the input directory")
parser.add_argument('-o', '--output-dir', required=True, help="Path to the output directory")

args = parser.parse_args()

if not os.path.isdir(args.input_dir):
    raise NotADirectoryError(f"Input directory does not exist: {args.input_dir}")
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir, exist_ok=True)

os.chdir(args.input_dir)

# Funktion til at finde værdier i XML-filer og gemme deres elementnavne og indhold
def Autosave_parser(filepath):
    liste = []  # laver en tom liste 
    for file in glob.glob("**\\*.xml", recursive=True):  # kigger efter alle XML-filer og kan gå igennem flere mapper
        with open(file, "rb") as autofile:  # Åbner XML-fil i binær
            root = ET.fromstring(autofile.read())  # Læser XML-indholdet ved brug af ET
            # kigger igennem alle elementer i XML-filen
            for i, paths in enumerate(root.findall(".//*")):
                # Bruger regex til at skille og sortere namespace fra tag-navnet så det nemmere at læse
                result = re.search("({.*})(.*)", f'{paths.tag} {paths.text}')
                # Tilføjer resultatet, sammen med indekset, til listen
                liste.append((result.group(2), i))
            return liste  
                
def writeoutput(outputpath, liste): #Funktion, som skriver resultaterne til en tekstfil i output-mappen
    with open(outputpath + "\\Autosavedata.txt", "w") as Auto:
        for stuff in liste:
            Auto.write(f"{stuff}\n") #løber igennem listen med resultater og skriver værdierne til filen.
Autosaveoutput = Autosave_parser(args.input_dir) #renamer første funktion og fortæller den argumentet den skal tage (input mappen)
#kalder den sidste funktion med 2 argumenter, første vores outputpath og 2 argument svare til den første funktion og den output.
writeoutput(args.output_dir, Autosaveoutput)               
