#!/usr/bin/env python3

from urllib.request import urlopen
import shutil
import traceback
import os
import sys

def download_file(file_url,file_name,dest_dir):
    http_response = urlopen(file_url)
    os.makedirs(dest_dir,exist_ok=True)
    with open(f'{dest_dir}/{file_name}',mode='wb') as f:
        f.write(http_response.read())
    
def main():
    download_file('https://raw.githubusercontent.com/remkop/picocli/main/src/main/java/picocli/CommandLine.java',
                  'CommandLine.java',
                  './picocli'
                 )                  

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        