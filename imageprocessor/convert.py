from subprocess import PIPE , run
import os
def extract_pages(up_file ):
    if not up_file :
        raise Exception ("Either upfile is invalid")
    pageextractor_args = ["python3","./page_extractor/page_extractor.py","-i",up_file]
    proc = run(pageextractor_args, stdout=PIPE, stderr=PIPE, encoding="utf-8")
    if proc.returncode != 0:
        print("Error Occured While extracting pages from images") #DEBUG
        raise Exception("page_extractor returned non zero code !" , proc)
    print("Extracted Pages..")

def convert_to_pdf(up_file,down_file):
    if not up_file or not down_file:
        raise Exception ( f"up_file : {up_file} Down_file: {down_file}")

    files =list(os.listdir(up_file))
    print(files)
    files_abs_list  = list(map(lambda y:os.path.join(up_file,y),files))
    args = ["img2pdf",*files_abs_list,"-o",down_file]
    proc = run(args,stdout = PIPE ,stderr = PIPE , encoding='utf-8')
    if proc.returncode !=0:
        print("Error!",proc)
        raise Exception("img2pdf returned non zero code : ",proc)
    else:
        print("Converted To pdf..",down_file)  #DEBUG
