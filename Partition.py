'''
QUEEN'S UNIVERSITY
CISC 365 2015F
Assignment 1
Brianna Rubin

This program uses the class Project to store each project as an object with
a name, start, finish, and weight(cost). The projects are sorted by start time,
and the first project that overlaps S is chosen. After this, addProjects
checks to see if the next-next-project overlaps with the current one. If not,
the next-project must be chosen or else there will be a gap where no projects
take place. If there is an overlap, then the algorithm recurses, only this time
the list of available projects begins at the second project in the list. It does
this until there are only 2 projects remaining, at which point it chooses either
the only safe choice, or the choice with a later finish time.

The Partition function creates a list of all the subsets of the chosen projects.
It then makes a list of all the sums of weights/costs of these subsets, and creates
a dictionary key for each sum with a value of the subset with that sum. It checks
the list of sums to find if one is equal to the target, which is 1/2 the sum of all
the chosen project costs. If not, it lowers the target by 1 until it is equal to a
sum in sumList. When one is found, the subset with that sum becomes Group 1.
and the remaining projects in the list of choen projects becomes Group2. and
'''


#create object class Projects
class Project:
        def __init__(self, name, start, finish):
                self.name = name
                self.s = start
                self.f = finish
                self.weight = finish - start

def main():

        #***************** FILE I/O *******************#

        myFile = open("SpaceStation.txt")
        lines = []
        A = []
        for line in myFile:
                newLine = str.split(line)
                lines.append(newLine)
        lines = lines[2:]

        #create list A of projects with a name, start, and finish
        for p in lines:
                A.append(Project(int(p[0]), int(p[1]), int(p[2])))

        #define S and F
        start = 20
        end = 100

        #********* SORT LIST BASED ON START TIME ********#

        sortedA = sorted(A, key=lambda x: x.s, reverse=False)

        #remove all projects that finish before F
        while sortedA[0].f < start:
                sortedA.pop(0)

        length = end - start + 1

        #start by adding first project
        chosenProjects = [sortedA[0]]

        #**** ADD PROJECTS AND PRINT SELECTED PROJECTS *****#

        chosenProjects = addProjects(sortedA, chosenProjects, sortedA[0])
        projectString = "Selected Projects:    "
        for p in chosenProjects:
                projectString += str(p.name)
                projectString += "    "
        print projectString

        #******* RUN PARTITION AND PRINT DATA ********#
        outputStrings = partition(chosenProjects)
        print outputStrings[0]
        print outputStrings[1]

def addProjects(list,chosen,current):
        i = 0
        if len(list) == 0:
                return chosen
        elif len(list) <= 1:
                chosen.append(list[0])
                return chosen
        if len(list) == 2:
                if list[1].s > list[0].f:
                        chosen.append(list[0])
                else:
                        if list[1].f > list[0].f:
                                chosen.append(list[1])
                        else:
                                chosen.append(list[0])
        else:
                if list[i+2].s > current.f:
                        chosen.append(list[i+1])
                        addProjects(list[1:],chosen,list[i+1])
                else:
                        addProjects(list[1:], chosen,current)
        return chosen

def partition(chosen):
        totalSum = 0
        for e in chosen:
                totalSum += e.weight
        target = totalSum / 2
        sumList = []
        subsetList = {}
        i = 0
        Subsets = reduce(lambda z, x: z + [y + [x] for y in z], chosen, [[]])
        for subset in Subsets:
                sum = 0
                for element in subset:
                        sum += element.weight
                sumList.append(sum)
                subsetList[sum] = subset
        while target > 0:
                if target in sumList:
                        closestSum = target
                        target = 0
                else:
                        target -= 1

        #********** FORMAT OUTPUT **********#

        Group1 = subsetList[closestSum]
        Group1Weight = 0
        Group1String = "Group 1  Projects:    "
        for project in Group1:
                Group1String += str(project.name)
                Group1String += "    "
                Group1Weight += project.weight
        Group1String += "                  Total Time: "
        Group1String += str(Group1Weight)
        #print Group1String
        del subsetList[closestSum]

        Group2 = chosen
        for p in Group2:
                if p in Group1:
                        Group2.remove(p)
        Group2Weight = 0
        Group2String = "Group 2  Projects:    "
        for project in Group2:
                Group2String += str(project.name)
                Group2String += "    "
                Group2Weight += project.weight
        Group2String += "                  Total Time: "
        Group2String += str(Group1Weight)
        #print Group2String
        output = [Group1String, Group2String]
        return output

main()
