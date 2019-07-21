import subprocess
import wget
import sys
import csv


domain = 'https://cheildigitaltechnologies.net/2019/ngo/uploads/'
imagename = sys.argv[1]
destinationpath = "D:/python/facematch/unknown/"+ imagename
filename = wget.download(domain+imagename, destinationpath)


location = imagename.replace('.jpeg','').split("-_-",2) #maxsplit


#file_ = open("D:/python/facematch/output.txt", "a+")
file_ = open("D:/python/facematch/tmp.txt", "w")
p = subprocess.Popen("face_recognition --tolerance 0.5 D:/python/facematch/known "+destinationpath, stdout=file_)
p.communicate() #now wait plus that you can send commands to process


listline =  list()
unmatcheddata = {}
with open('D:/python/facematch/missingdata.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        unmatcheddata[row[0]] = row



with open('D:/python/facematch/log.txt', 'a+') as log_file:
    with open("D:/python/facematch/tmp.txt", "r") as f:
        for line in f:
            # print(line)
            log_file.write(line)
            if (",unknown_person" not in line) and (",no_persons_found" not in line):
                person_name = line.split(",line")
                listline.append(person_name[0])
            

name =  ""
with open('D:/python/facematch/output.txt', 'w') as output_file:
    output_file.write("")
    if len(listline) > 0:
        output_file.write("Hi <br /><br />There is a new lead by iPath. <br /><br />Person matched with below missing people.<br /><br />")#Maching Person Image URL :" + domain + imagename 
        output_file.write("<br />Google Map URL  : https://www.google.com/maps/place/@"+location[1]+","+location[2]+",20z<br /><br />")
        for fLine in listline:
            name = fLine.split(",")[1].replace('\n', '')
            output_file.write('<table cellpadding=5 cellspacing=0 border=1 width=\'600\'>')
            output_file.write('<tr><td style="text-align:center;color:#000000;background:#42ff00;font-weight:bold">Matching Person Image</td><td style="text-align:center;color:#000000;background:#ff6900;font-weight:bold">Missing Person Image</td></tr>')
            output_file.write('<tr><td style="text-align:center"><img src="' +domain+imagename + '" width="200" /></td><td style="text-align:center"><img src="https://cheildigitaltechnologies.net/2019/ngo/known/'+name + '.jpg" width="200" /></td></tr>')
            output_file.write('</table><br />')
            output_file.write('<table cellpadding=5 cellspacing=0 border=1 width=\'600\'>')
            output_file.write('<tr><td>Missing Person Name  :</td><td>' + unmatcheddata[name][1] + '</td></tr><tr><td>City  :</td><td>' + unmatcheddata[name][8] + '</td></tr>')
            output_file.write('<tr><td>Gurdian\'s Name  :</td><td>' + unmatcheddata[name][2] + '</td></tr><tr><td>Age  :</td><td>' + unmatcheddata[name][3] + '</td></tr><tr><td>Gender  : </td><td>' + unmatcheddata[name][4] + '</td></tr>')
            output_file.write('<tr><td>GDE No  : </td><td>' + unmatcheddata[name][5] + '</td></tr><tr><td>GDE Date  :</td><td>' + unmatcheddata[name][6] + '</td></tr><tr><td>State  :</td><td>' + unmatcheddata[name][7] + '</td></tr>')
            output_file.write('<tr><td>District  :</td><td>' + unmatcheddata[name][8] + '</td></tr><tr><td>Police Station  :</td><td>' + unmatcheddata[name][9] + '</td></tr><tr><td>Mobile  :</td><td>' + unmatcheddata[name][10] + '</td></tr>')
            output_file.write('<tr><td>Phone  :</td><td>' + unmatcheddata[name][11] + '</td></tr><tr><td>Email  :</td><td>' + unmatcheddata[name][12] + '</td></tr>')
            output_file.write('</table><br />')
        output_file.write("<a href='D:/RPAProject/iPath/verifyresult.bat'>Click here</a> to verify the result!<br/>")
        output_file.write('<br>Best,<br />Team iPath')

with open('D:/python/facematch/checkfile.txt', 'w') as output_file:
    output_file.write(domain+imagename+"|"+"https://cheildigitaltechnologies.net/2019/ngo/known/" + name + ".jpg")

print("\nProcess Done")

