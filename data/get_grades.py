import csv

cse = []
mat = []
others = []
grades = []
cgpa = []

output = open("output_grades.txt","w")

with open('grades.csv') as file_obj:
    reader_obj = csv.reader(file_obj)

    for row in reader_obj:
        grades.append(row[2])
        cgpa.append(float(row[3]))
        
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
        output.write("   | " + " | ".join(row) + " |\n")


output.write("###CSE courses###\n")
show_table(cse)

output.write("###MNS courses###\n")
show_table(mat)

output.write("###GenEd courses###\n")
show_table(others)

output.write("\nOverall cgpa: " + str(sum(cgpa) / len(cgpa)) + " and Total number of course: "+str(len(cgpa)))