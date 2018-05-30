#This file combs through the MIND data, and gathers all the participant information, creates a CSV

import glob, os, argparse, re, csv

#setting up script:
parser = argparse.ArgumentParser(description = "Takes as its first argument the path to the directory containing input transcripts, and as its second argument the path to the directory for the output CSVs")
parser.add_argument('input_dir' , type=str, help='location of files to process')
parser.add_argument('output_dir' , type=str, help='location for output CSVs')
args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#patterns:
pattern1 = re.compile("^[$+]") #noting all participant data
pattern2 = re.compile("^(\$ *)(.*)") #participants
pattern3 = re.compile("^(\+ *[Ll][Aa][Nn][Gg][Uu][Aa][Gg][Ee]: *)(.*)") #language
pattern4 = re.compile("^(\+ *[Pp][Aa][Rr][Tt][Ii][Cc][Ii][Pp][Aa][Nn][Tt][Ii][Dd]: *)(.*)") #participant id
pattern5 = re.compile("^(\+ *[Dd][Oo][Ee]: *)(.*)") #DOE, date of examination
pattern6 = re.compile("^(\+ *[Cc][Oo][Nn][Tt][Ee][Xx][Tt]: *)(.*)") #Context (ADOS, Con, Nar)
pattern7 = re.compile("^(\+ *[Tt][Rr][Aa][Nn][Ss][Cc][Rr][Ii][Bb][Ee][Rr]: *)(.*)") #Transcriber name
pattern8 = re.compile("^(\+ *[Ll][Ss][Ii][Dd]: *)(.*)") #LSID
pattern9 = re.compile("^(\+ *[Dd][Oo][Tt]: *)(.*)") #DOT, date of transcription
pattern10 = re.compile("^(\+ *[Dd][Oo][Uu][Bb][Ll][Ee][Cc][Hh][Ee][Cc][Kk][Ee][Rr]: *)(.*)") #Doublechecker, name and date
pattern11 = re.compile("^(\+ *[Nn][Oo][Tt][Ee][Ss]: *)(.*)") #Notes
pattern12 = re.compile("^(\+ *[Ss][Tt][Uu][Dd][Yy]: *)(.*)") #Study
pattern13 = re.compile("^(\+ *[Tt][Ii][Mm][Ee]: *)(.*)") #Time
pattern14 = re.compile("^(\+ *[Vv][Ee][Rr][Ss][Ii][Oo][Nn]: *)(.*)") #Version, A or B
pattern15 = re.compile("^(\+ *[Cc][Oo][Mm][Pp][Ll][Ee][Tt][Ii][Oo][Nn]: *)(.*)") #Completion status
patterns = [pattern2, pattern3, pattern4, pattern5, pattern6, pattern7, pattern8, 
            pattern9, pattern10, pattern11, pattern12, pattern13, pattern14, pattern15]
pattern16 = re.compile("^(.*)(P)")
pattern17 = re.compile("^(.*)(O)")
#main work:
with open(output_dir + "participant_data.csv", 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name_of_File", "Individuals_Present", "Language", "Participant_ID", 
            "DOE", "Context", "Transcriber", "LSID", "DOT", "Doublechecker", "Notes", 
            "Study", "Time", "Version", "Completion"])
        for file in glob.glob(input_dir+"*/*.txt"):
            with open(file, "r") as f:
                #initializing the row:
                data_items = [file]
                for i in range(1,15):
                    data_items.append("Field Missing")
                #adding the information we have:
                for line in f:
                    temp_patterns = patterns
                    line = line.replace("\ufeff", "")
                    line = line.strip()
                    if re.match(pattern1, line):
                        for pattern in patterns:
                            if re.match(pattern, line):
                                data_items[patterns.index(pattern)+1] = re.match(pattern, line).group(2)
                                break
                    else:
                        break
            writer.writerow(data_items)  

with open(output_dir + "files_with_parent_otherexaminer.csv", "w+", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name_of_File", "Parent_Present", "Other_Examiner_Present"])
    for file in glob.glob(input_dir+"*/*.txt"):
        with open(file, "r") as f:
            data_items = [file, "0", "0"]
            for line in f:
                line = line.replace("\ufeff", "")
                line = line.strip()
                if re.match(pattern2, line):
                    participants = re.match(pattern2, line).group(2)
                    if re.match(pattern16, participants):
                        data_items[1] = "1"
                    if re.match(pattern17, participants):
                        data_items[2] = "1"
                    break
        writer.writerow(data_items)            

