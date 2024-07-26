#oop concepts in python;

#Creating Class Learner
class Learner:
    def  __init__(self, name, programme):
        self.learner_name = name
        self.programme = programme

    def __str__(self):
        return f"My name is:{self.learner_name},  Pursuing:{self.programme}"
    

#Creating child class Student that inherits Base class Learner
class Student(Learner):
    def __init__(self, name, programme, Region, Age, Student_id):
        super().__init__(name, programme)
        self.region = Region
        self.age = Age
        self.student_id = Student_id
        self.skills = []
        

    def passed_skills (self, *skills):
        for skill in skills:
            self.skills.append(skill)

    def __str__(self):
        skill_add = ', '.join(self.skills)
        return f"My name is {self.learner_name}, Specializing in: {self.programme}, I am from {self.region}, Age: {self.age},  Student_id: {self.student_id}, Skilled in: {skill_add}"

L1 = Learner("", "BE")
print(L1) 

Student1  = Student(f"koula" ,"BE" , "Africa, Kenya", 22, 2190)
Student1.passed_skills("Python", "mysql")
print(Student1)


#Polymorphism

class Undergraduate(Learner):      
    def __init__(self, name,Programme, major):
        super().__init__(name, Programme)
        self.major = major
        self.skills = []
        
    
    def passed_skills(self, *skills):
        if len(skills) < 2:
            self.skills.extend(skills)
            return f"Skills added: {', '.join(skills)}"
        else:
            return f"Name: {self.learner_name}, Major: {self.major} . Skill list should at-least be one" 
        
    def __str__(self):
            skill_add = ', '.join(self.skills)
            return f"Name: {self.learner_name}, Major: {self.major}  "
        

Grad = Undergraduate("Glow", "BE", "Computer Science")
print(Grad)
print(Grad.passed_skills("Python"))
print(Grad.passed_skills("MySQL", "Data Analysis"))
print(Grad)

