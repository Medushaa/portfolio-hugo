import csv

cse = []
mat = []
others = []
grades = {'A+':0, 'A':0, 'A-':0, 'B+':0, 'B':0}
cgpa = []

output = open("output_grades.txt","w")

links = {}
with open('note-links.csv') as file_obj:
    reader_obj = csv.reader(file_obj)

    for row in reader_obj:
        links[row[0]] = row[1]


with open('grades.csv') as file_obj:
    reader_obj = csv.reader(file_obj)

    for row in reader_obj:
        grades[row[2]] += 1
        cgpa.append(float(row[3]))
        if row[0] in links.keys():
            row.append(links[row[0]])
        else:
            row.append("None")
        
        if len(row[1])>30:
            row[1] = row[1][:30] + "..."
        else:
            row[1] = row[1] + (33 - len(row[1]))*(" ")
    
        if row[0][:3] == "CSE":
            cse.append(row)
        elif row[0][:3] == "MAT":
            mat.append(row)
        else:
            others.append(row)
        

def show_table(courses):
    for row in courses:
        if row[4] == "None":
            output.write("   | " + " | ".join(row[:4]) + " | (No Notes) |\n")
        else:
            output.write("   | " + " | ".join(row[:4]) + " | [Note Link](" + row[4] + ") |\n")



output.write("###CSE courses###\n")
show_table(cse)

output.write("###MNS courses###\n")
show_table(mat)

output.write("###GenEd courses###\n")
show_table(others)

output.write("\nOverall cgpa: " + str(sum(cgpa) / len(cgpa)) + " and Total number of course: "+str(len(cgpa)))

print(grades)

