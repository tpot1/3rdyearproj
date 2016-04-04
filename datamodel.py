import random
import numpy

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *

#i = open('interestValues.txt', 'r')
# for ii in range(0, 167):
# 	i.write(str(random.uniform(0, 1)))
# 	i.write("\n")

#list of grades using values obtained from COMP1202 class of 2013/14
engagedGrades = [100,98,96,95,94,93,91,90,89,88,86,85,84,82,81,80,79,79,79,78,78,78,77,77,76,76,75,75,74,74,73,73,72,72,72,71,71,71,70,70,70,69,69,69,68,68,68,67,67,67,66,66,66,65,65,65,64,64,64,63,63,63,62,62,62,61,61,61,60,60,60]
samplingGrades = [79,78,78,77,77,76,76,75,75,74,74,73,73,72,72,71,71,70,70,69,68,67,66,65,64,63,62,62,61,61,60,60,59,59,58,58,57,57,56,56,55,55,54,54,53,53,52,52,52,51,51,51,50,50,50,49,49,48,48,47,47,46,46,45,45,44,43,42,41,40,39,37,35,33,31]
disengagedGrades = [47,46,45,44,43,42,41,40,39,36,33,30,27,24,21,20,19,18,17,16,15,14,13,12,11]


# eg = open('engagedGradeOrder.txt', 'w+')
# l = range(0, len(engagedGrades))
# random.shuffle(l)
# for i in range(0,len(l)):
# 	eg.write(str(l[i]))
# 	eg.write("\n")
# eg.close()

# dg = open('disengagedGradeOrder.txt', 'w+')
# l = range(0, len(disengagedGrades))
# random.shuffle(l)
# for i in range(0,len(l)):
# 	dg.write(str(l[i]))
# 	dg.write("\n")
# dg.close()

# sg = open('samplingGradeOrder.txt', 'w+')
# l = range(0, len(samplingGrades))
# random.shuffle(l)
# for i in range(0,len(l)):
# 	sg.write(str(l[i]))
# 	sg.write("\n")
# sg.close()

with open("interestValues.txt") as f:
    interestValues = f.readlines()
interestCounter = 0

with open("engagedGradeOrder.txt") as f:
	engagedGradeOrder = f.readlines()

with open("disengagedGradeOrder.txt") as f:
	disengagedGradeOrder = f.readlines()

with open("samplingGradeOrder.txt") as f:
	samplingGradeOrder = f.readlines()

gradeCounter = 0

# Bounds of attendance rate of each category
disAtt = [0.005, 0.25]
sampAtt = [0.25, 0.65]
attAtt = [0.65, 1.0]

# Number of weeks which the system models
numberWeeks = 12


# Dampening value representing how imperfect application is
effect = 0.1

# value representing the number of students still using the system by the end of term
percentageUninterested = 0.6

# Value representing effect increased attendance has on grades
# so going to 100% more lectures increases your grade by gradeEffect
gradeEffect = 1.68

students = []
attendances = []
grades = []

class Student:
    def __init__(self, category, interest, attendance, grade):
        self.category = category
        self.interest = interest
        self.attendance = attendance
        self.grade = grade

# generates students - uses random value between 0 and 1 for effect of gamification on that student
for i in range(0, len(disengagedGrades)):
	grade = disengagedGrades[int(disengagedGradeOrder[gradeCounter])]
	attendance = disAtt[0] + (((disAtt[1]-disAtt[0])/len(disengagedGrades))*i)
	s = Student(0, interestValues[interestCounter], attendance, grade)
	interestCounter += 1
	gradeCounter += 1
	students.append(s)
	attendances.append(attendance)
	grades.append(grade)

gradeCounter = 0
for i in range(0, len(samplingGrades)):
	grade = samplingGrades[int(samplingGradeOrder[gradeCounter])]
	attendance = sampAtt[0] + (((sampAtt[1]-sampAtt[0])/len(samplingGrades))*i)
	s = Student(1, interestValues[interestCounter], attendance, grade)
	interestCounter += 1
	gradeCounter += 1
	students.append(s)
	attendances.append(attendance)
	grades.append(grade)

gradeCounter = 0
for i in range(0, len(engagedGrades)):
	grade = engagedGrades[int(engagedGradeOrder[gradeCounter])]
	attendance = attAtt[0] + (((attAtt[1]-attAtt[0])/len(engagedGrades))*i)
	s = Student(2, interestValues[interestCounter], attendance, grade)
	interestCounter += 1
	gradeCounter += 1
	students.append(s)
	attendances.append(attendance)
	grades.append(grade)


bgradeSum = 0
battendanceSum = 0

bdisGradeSum = 0
bdisAttSum = 0
bdisCounter = 0

bsampGradeSum = 0
bsampAttSum = 0
bsampCounter = 0

battGradeSum = 0
battAttSum = 0
battCounter = 0

bdropouts = 0

for student in students:
	bgradeSum += student.grade
	battendanceSum += student.attendance

	if student.grade < 40:
		bdropouts += 1

	if student.category == 0:
		bdisCounter += 1
		bdisGradeSum += student.grade
		bdisAttSum += student.attendance

	elif student.category == 1:
		bsampCounter += 1
		bsampGradeSum += student.grade
		bsampAttSum += student.attendance

	elif student.category == 2:
		battCounter += 1
		battGradeSum += student.grade
		battAttSum += student.attendance

uninterestedStudents = []
newAttendances = []
newGrades = []

trace0 = go.Scatter(
	   x = attendances,
	   y = grades,
	   mode = 'markers',
	   marker=go.Marker(
	            color='red',
	            symbol='square'
	        )
	)

data = [trace0]

def timestep(time):
	newAttendances = []
	newGrades = []
	threshold = time * (percentageUninterested/numberWeeks)
	for student in students:
		if student not in uninterestedStudents:
			# if the student's interest in the system is below the threshold, they stop using the system
			if student.interest < threshold:
				uninterestedStudents.append(student)
			else:
				oldAttendance = student.attendance

				# calculates new attendance rate by adding the product of the base effect value and the maximum effect of the application on the student (i.e. the effect required to reduce optional absenses to 0)
				newAttendance = student.attendance + (effect * ((0.6*(1.0-oldAttendance))/numberWeeks))
				if newAttendance > 1:
					newAttendance = 1
				newAttendances.append(newAttendance)
				student.attendance = newAttendance

				# percentage increase in lecture attendance - so students with lower original attendance benefit more
				difference = (newAttendance / oldAttendance) - 1.0

				#calculates new grade by adding the product of the increase in the students attendance rate by the grade effect value
				newGrade = student.grade + (difference * gradeEffect)
				if newGrade > 100:
					newGrade = 100
				newGrades.append(newGrade)	
				student.grade = newGrade	

	trace = go.Scatter(
	   x = newAttendances,
	   y = newGrades,
	   mode = 'markers',
	   marker=go.Marker(
	   		color='rgb(' + str(i*5) + ',' + str(i*5) + ',256)'
	        )
	)

	data.append(trace)

for i in range(0, numberWeeks):
	timestep(i)


#Plot and embed in ipython notebook
py.iplot(data, filename='expected attendance vs exam results')

agradeSum = 0
aattendanceSum = 0

adisGradeSum = 0
adisAttSum = 0
adisCounter = 0

asampGradeSum = 0
asampAttSum = 0
asampCounter = 0

aattGradeSum = 0
aattAttSum = 0
aattCounter = 0

adropouts = 0

for student in students:
	agradeSum += student.grade
	aattendanceSum += student.attendance

	if student.grade < 40:
		adropouts += 1

	if student.category == 0:
		adisCounter += 1
		adisGradeSum += student.grade
		adisAttSum += student.attendance

	elif student.category == 1:
		asampCounter += 1
		asampGradeSum += student.grade
		asampAttSum += student.attendance

	elif student.category == 2:
		aattCounter += 1
		aattGradeSum += student.grade
		aattAttSum += student.attendance

print("\t\t\t\tBEFORE\t\tAFTER")
print("Average Overall Grade: " + "\t\t" + str(bgradeSum/len(students)) + "\t\t" + str(agradeSum/len(students)))
print("Average Overall Attendance: " + "\t" + str((battendanceSum/len(students))*100) +"%" + "\t" + str((aattendanceSum/len(students))*100) + "%")
print("Number of drop-outs: " + "\t\t" + str(bdropouts) + "\t\t" + str(adropouts))
print("")
print("Average Disengaged Grade: " +  "\t" + str(bdisGradeSum/bdisCounter) + "\t\t" + str(adisGradeSum/adisCounter))
print("Average Disengaged Attendance: " + "\t" + str((bdisAttSum/bdisCounter)*100) + "%" + "\t\t" + str((adisAttSum/adisCounter)*100) + "%")
print("")
print("Average Sampler Grade: " + "\t\t" + str(bsampGradeSum/bsampCounter) + "\t\t" + str(asampGradeSum/asampCounter))
print("Average Sampler Attendance: " + "\t" + str((bsampAttSum/bsampCounter)*100) + "%" + "\t" + str((asampAttSum/asampCounter)*100) + "%")
print("")
print("Average Engaged Grade: " + "\t\t" + str(battGradeSum/battCounter) + "\t\t" + str(aattGradeSum/aattCounter))
print("Average Engaged Attendance: " + "\t" + str((battAttSum/battCounter)*100) + "%" + "\t" + str((aattAttSum/aattCounter)*100) + "%")


# bear in mind I am modelling overall attendance rather than attendance at specific weeks
# so I don't need to model attendance gradually decreasing as the term goes on, or 
# decreasing at coursework deadlines, because I am just concerned with the overall attendance.
# Confusing because I am modelling it week by week, but this is just to show that some will 
# stop using the application part way through. 


# Assumptions:
# Overall Attendance ~56% (following data found in *source*)

# Variables:
# Effect of increased attendance on grades - from 1% to 5%?
# maximum effect values of each category 
# ---should have an effect of ~24.6% (60% of absenses) on samplers, as these represent the majority of users
# ---should have a higher effect on disengaged, and lower on engaged
# dampening value - represents how well the applition works - 100% means no users will miss any lectures for illegitimate reasons
# ---should range from maybe 10% to 50%, don't want to be too ambitious
# Number of students that lose interest - depends on how good the application is - from 30% to 60%?
# ---research categories of gamers, and number of people that arent interested?