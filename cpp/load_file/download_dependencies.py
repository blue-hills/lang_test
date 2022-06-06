#!/usr/bin/env python3

from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import shutil
import os
import sys
import traceback
  
def extract_directory_from_zip_url(url,directory, dest_dir='.'):
    http_response = urlopen(url)
    os.makedirs(dest_dir,exist_ok=True)
    with ZipFile(BytesIO(http_response.read())) as zipfile:
        for file in zipfile.namelist():
            if file.startswith(directory):
                zipfile.extract(file,path=dest_dir)

def get_third_party_src(third_party_zip_url,folder_to_copy,dest_folder,folder_to_remove):
    extract_directory_from_zip_url(third_party_zip_url,folder_to_copy)
    os.makedirs(dest_folder,exist_ok=True)
    shutil.rmtree(dest_folder)
    shutil.copytree(f'./{folder_to_copy}',dest_folder)
    shutil.rmtree(folder_to_remove,ignore_errors=True)    
    
def main():
    extract_directory_from_zip_url(
        'https://boostorg.jfrog.io/artifactory/main/release/1.79.0/source/boost_1_79_0.zip',
        'boost_1_79_0/boost',
        './third_party/'
        )
    print('Define BOOST_SOURCE either as an environment variable or cmake -D variable as follows:')
    print('export BOOST_SOURCE=./third_party/boost_1_79_0/')
    print('cmake -DBOOST_SOURCE=./third_party/boost_1_79_0/')
              
    get_third_party_src('https://github.com/fmtlib/fmt/archive/refs/heads/master.zip',
                        'fmt-master/include/',
                        'third_party/fmt-master/include/',
                        './fmt-master'
                       )
    
    get_third_party_src('https://github.com/p-ranav/argparse/archive/refs/heads/master.zip',
                        'argparse-master/include/',
                        './third_party/argparse-master/include/',
                        './argparse-master'
                       )              
    print('Define THIRD_PARTY_SOURCE as an environment or cmake Define variable as follows')
    print('export THIRD_PARTY_SOURCE=./third_party/')
    print('cmake -DTHIRD_PARTY_SOURCE=./third_party/')
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        