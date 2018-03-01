import csv
import argparse
import json
import re

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="CSV to JSON")
    parser.add_argument("-i",
                        "--inputfile",
                        dest="input",
                        help="File name of the input csv file",
                        default=None)
    parser.add_argument("-a",
                        "--attributes",
                        dest="attrib",
                        help="Attributes to include in the output json file",
                        default="id,text,created_at,place,coordinates")

    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    if args.input == None:
        print("Error: No input file selected. See the README.md file for more information.")
    else:
        a = args.attrib.split(",")
        with open(str(args.input)+'.csv', 'w') as o:
            writer = csv.DictWriter(o, fieldnames=a)
            writer.writeheader()
            with open(str(args.input)+'.json', 'r') as f:
                for line in f:
                    reader = json.loads(line)#, fieldnames="text")
                    lineAdd = []
                    for t in a:
                        hold = reader[t]
                        if t == "text":
                            txt = ''.join((hold)).encode('utf-8').strip()
                        else:
                            txt = hold
                        txt = str(txt).decode('unicode_escape').encode('ascii','ignore')
                        txt = txt.replace("\n", "").replace("\r", "").replace("\t","")
                        txt = re.sub(' +', ' ', txt)
                        txt = txt.replace('\.+','.')
                        lineAdd.append(txt)
                    writer.writerow({a[i]: lineAdd[i] for i in range(len(lineAdd))})

