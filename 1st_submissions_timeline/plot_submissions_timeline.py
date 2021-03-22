#!/usr/bin/env python3

import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests as req
from datetime import datetime

OK = '\033[92m'             #verde
ERR = '\033[91m'            #rojo
INFO = '\033[94m'           #azul
ENDC = '\033[0m'            #end color
BOLD = '\033[1m'            #bold!

if len(sys.argv[1:]) != 3:
    print(f'\n{BOLD}{ERR}[!] Los tres parametros son necesarios!{ENDC}\n')
    print(f'{BOLD}{INFO}[*] Ej: {sys.argv[0]} apikey hash [year|month|day] {ENDC}\n')
    exit()

apikey = sys.argv[1]
hashfile = sys.argv[2]
freq = sys.argv[3]

assert freq in ['year', 'month', 'day'], 'Unicamente se pueden usar las opciones "year", "month" o "day"\n'

print(f"""{OK}
===========================================================================================
Genera un timeline de archivos similares en VirusTotal a partir de un hash
* Fecha de 'First Submission'
* Ultimos 40 archivos analizados en VT
===========================================================================================
USO: python3 {sys.argv[0]} apikey hash [year|month|day]
===========================================================================================
{ENDC}""")

def plot_submissions_timeline(apikey, hashfile, freq):
    vt3_response = req.get(f'https://www.virustotal.com/api/v3/files/{hashfile}/similar_files?limit=40', headers={'x-apikey': apikey}, verify=True).json()
    date_format={'year':'%Y-%m-%d', 'month':'%Y-%m', 'day':'%Y-%m-%d'}
    first_subm_dates = [datetime.utcfromtimestamp(int(f['attributes']['first_submission_date'])).strftime(date_format[freq]) for f in vt3_response['data']]
    first_subm_dates.sort()
    sns.set(rc={'figure.figsize':(18,8)})
    sns.set_style('darkgrid')
    sns.countplot(x=first_subm_dates, palette=['#432371',"#FAAE7B"]).set_title('Historial de Similar Files Submissions (First Submissions)', fontsize=22)
    plt.xticks(rotation=45)
    plt.show(block=True)


if __name__ == '__main__':
    try:
        plot_submissions_timeline(sys.argv[1], sys.argv[2], sys.argv[3])
    except KeyboardInterrupt:
        print(f'{BOLD}{ERR}[!] Terminando script...{ENDC} ')
        exit()