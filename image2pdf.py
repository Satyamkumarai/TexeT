import argparse
import img2pdf
import sys
parser = argparse.ArgumentParser()

parser.add_argument("-f","--file")

if __name__=='__main__':
    parsed = parser.parse_args()
    
    if 'file' in parsed:
        filename = parsed.file
    else:
        raise Exception("File not Found Error")
    
    
