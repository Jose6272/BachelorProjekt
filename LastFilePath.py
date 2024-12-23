#!/usr/bin/python3
from xml.etree import ElementTree as ET # libary som kan arbejde med xml-filer
import argparse #Libary som håndtere kommandolinje argumenter
import glob #libary som kan finde filer med mønstre
import os # libary til at arbejde med fil og mappe placeringer

#Parser som kigger i user.config filen som ISE laver og finder feltet i xml dokumentet som hedder Lastfile path.

#kodestykke som fortæller hvilke argumenter som koden kan tage.
parser = argparse.ArgumentParser(description="Process input and output directories.")
parser.add_argument('-i', '--input-dir', required=True, help="Path to the input directory")
parser.add_argument('-o', '--output-dir', required=True, help="Path to the output directory")

#læser argumenterne 
args = parser.parse_args()

#chekker om input mappen findes og hvis ikke skriv fejl mappen findes ikke
if not os.path.isdir(args.input_dir):
    raise NotADirectoryError(f"Input directory does not exist: {args.input_dir}")
if not os.path.exists(args.output_dir): #chekker om output mappe findes og hvis ikke opretter den mappen. 
    os.makedirs(args.output_dir, exist_ok=True)

#skrifter den mappen som koden skal køre i, den skal "lade som om" at den køre fra inputmappen, 
# istedet for den mappe som den ligger i.     
os.chdir(args.input_dir)

#en funktion som kigger i user.config filen efter et felt med navnet lastfilepath.
def ISE_LFP_parser(filepath):
    liste = [] #tom liste
    for lastpath in glob.glob("**\\user.config", recursive=True): #kigger efter alle user.config filer og kan kigge ned i flere mapper ikke kun den den er i.
        with open(lastpath, "rb") as LFP: #åbner fil i binær form
            root = ET.fromstring(LFP.read()) #bruger ET til at læse xml filen
            for i,path in enumerate(root.findall(".//setting/[@name='LastFilePath']/value")): #finder lastfilepath i filen 
                liste.append((path.text,i)) #tilføjer den den finder til listen i text form samt et tal udfra linjerne. 
            return liste

#Funktion, som skriver resultaterne til en tekstfil i output-mappen
def writeoutput(outputpath, liste):
    with open(outputpath + "\\LastFilePath_data.txt", "w") as parsed: #opretter og åbner filen 
        for stuff in liste: #løber igennem listen med resultater og skriver værdierne til filen.
            parsed.write(f"{stuff}\n")
LED_parseroutput = ISE_LFP_parser(args.input_dir) #renamer første funktion og fortæller den argumentet den skal tage (input mappen)
#kalder den sidste funktion med 2 argumenter, første vores outputpath og 2 argument svare til den første funktion og den output.
writeoutput(args.output_dir, LED_parseroutput) 