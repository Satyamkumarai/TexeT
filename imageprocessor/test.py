from subprocess import PIPE , run 
import os 
upfile = "./30de5277-9866-408b-bb8a-d7bf3f8dc341"

files =list(os.listdir(upfile))
print(files)
filesabs  = " ".join (map(lambda y:os.path.join(upfile,y),files))
print(filesabs)
args = ["img2pdf",filesabs,"-o","output.pdf"]
proc = run(args,stdout = PIPE ,stderr = PIPE , encoding='utf-8')
if proc.returncode !=0:
    print("Error!",proc)
else:
    print("done!")

