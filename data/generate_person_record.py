#!/usr/bin/env python3

import requests
import random
import argparse
import traceback


API_KEY = None
MAX_FETCH_LIMIT  = 1000

def get_request_headers():
    return {'X-Api-Key':API_KEY}    

def generate_names(quantity):
    url = 'https://randommer.io/api/Name'
    params = {'nameType':'fullname','quantity':quantity}
    return requests.get(url,headers=get_request_headers(),params=params).json()
    
def generate_phone_numbers(quantity):
    url = 'https://randommer.io/api/Phone/Generate'
    params = {'CountryCode':'US','quantity':quantity}
    return requests.get(url,headers=get_request_headers(),params=params).json()


def generate_data(start_id,nitems,quote,f):
    names = generate_names(nitems)
    p_numbers = generate_phone_numbers(nitems)
    for i,item in enumerate(zip(names,p_numbers),start=start_id):
        age = random.randint(20,101)
        salary = random.randint(50,400)*1000
        if quote:
            name = item[0].split()
            print(f'{i} "{name[0]}" "{name[1]}" "{item[1][3:]}" {age} {salary}',file=f)       
        else:
            print(f'{i} {item[0]} {item[1][3:]} {age} {salary}',file=f)       

def get_args():
    argparser = argparse.ArgumentParser("DataGenerator",
         description="""Generates Data File (FirstName LastName PhoneNumber Age Salary) using https://randommer.io/ """)
    argparser.add_argument('-r','--records',type=int,default = 1000,help='Number of Records to be generated')
    argparser.add_argument('-o','--out',type=str,default='./out',help='Output File Path')
    argparser.add_argument('-k','--key',type=str,required=True,help='API Key to https://randommer.io/ ')
    argparser.add_argument('-q','--quote',type=bool,help='Write Quoted Strings',default=False)
    args = argparser.parse_args()
    return args

def main():
    args = get_args()
    global API_KEY
    API_KEY = args.key

    with open(args.out,mode='w') as f:
    # fetch records in batches as number of records per call cannot exceed MAX_FETCH_LIMIT
        loopcount = args.records//MAX_FETCH_LIMIT
        for batch in range(loopcount):
            generate_data(batch*MAX_FETCH_LIMIT+1,MAX_FETCH_LIMIT,args.quote,f)
            print(f'generated {(batch+1)*MAX_FETCH_LIMIT} ')
        remaining_rec = args.records %MAX_FETCH_LIMIT
        if remaining_rec != 0:
            generate_data(loopcount*MAX_FETCH_LIMIT+1,remaining_rec,args.quote,ef)
            print(f'generated {remaining_rec} ')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()

        
            

