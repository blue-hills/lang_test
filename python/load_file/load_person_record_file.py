#!/usr/bin/env python3

from dataclasses import Field, dataclass
from typing import ClassVar
import argparse
import re

@dataclass
class PersonRecord:
    person_id : int
    first_name : str
    last_name : str
    phone_number : str
    age : int
    salary : int 
    pr_regex : ClassVar[re.Pattern] = re.compile(r"\s*(\d+)\s+(\w+)\s+(\w+)\s+(\S+)\s+(\d+)\s+(\d+)")

    @staticmethod
    def parse(record : str):
        items = record.split()
        return PersonRecord( person_id=int(items[0]), first_name=items[1],last_name=items[2],
               phone_number=items[3],age=int(items[4]),salary=int(items[5]))
    
    @staticmethod
    def parse_regex(record : str):
        m = PersonRecord.pr_regex.search(record)
        if not m: 
            raise RuntimeError(f'could not parse {record}')
        return PersonRecord(person_id=int(m.group(1)), 
                            first_name=m.group(2),
                            last_name=m.group(3),
                            phone_number=m.group(4),
                            age=int(m.group(5)),
                            salary=int(m.group(6)))

def read_person_record_from_file(inputfile : str,parse_func):
    person_data = {}
    with open(inputfile,mode='r') as f:
        for line in f:
            person_record = parse_func(line)
            person_data[person_record.person_id] = person_record
    return person_data

def get_args():
    parser = argparse.ArgumentParser("ReadPersonRecordFile")
    parser.add_argument('-r','--repeat',type=int,default=1000,help='Repeat Count')
    parser.add_argument('-i','--input',type=str,required=True,help='Input file containing Person Records')
    parser.add_argument('-a','--algo',type=str,default='split',required=False,
                        choices=['split','regex'],help='Algorithm to parse person record')
    return parser.parse_args()

def main():
    args = get_args()
    parse_func = PersonRecord.parse_regex if args.algo == 'regex' else  PersonRecord.parse
    for _ in range(args.repeat):
        data_dict = read_person_record_from_file(args.input,parse_func)
        if (len(data_dict) -1) not in data_dict:
            raise RuntimeError(f'person_record for person_id = {args.repeat-1} not found')
    print(f'Executed {args.repeat} times successfully.')
    print(f'{"regex" if args.algo == "regex" else "str.split"} has been used for parsing.')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
