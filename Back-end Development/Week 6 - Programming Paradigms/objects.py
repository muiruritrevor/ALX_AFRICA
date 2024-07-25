#oop concepts in python;
'''Encapsulation'''
class Learner:
    def  __init__(self, name, programme):
        self.learner_name = name
        self.programme = programme

    def __str__(self):
        return f"My name is:{self.learner_name},  Pursuing:{self.programme}"

        
learner1 = Learner("Joe", "BE")
print(learner1)

'''#Inheritance'''

class Student(Learner):
    def __init__(self, Region, Age, Student_id):
       # super().__init__(name, programme)
        self.region = Region
        self.age = Age
        self.student_id = Student_id
        self.skills = []

    def info (self):
        self.skills.append(["Python", "MySQL"])
        return Student
    def __str__(self):
        return f"I am from {self.region}. Skilled in {self.info()}"
    

Student1  = Student(f"Africa,Kenya", "Python" , 2190)
print(Student1)

