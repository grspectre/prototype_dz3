from sqlalchemy import Column, Integer, String, ForeignKey, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Faculty(Base):
    __tablename__ = 'faculties'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    students = relationship("Student", back_populates="faculty")
    
    def __repr__(self):
        return f"<Faculty(name='{self.name}')>"

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculties.id'), nullable=False)
    
    faculty = relationship("Faculty", back_populates="students")
    grades = relationship("Grade", back_populates="student")
    
    def __repr__(self):
        return f"<Student(last_name='{self.last_name}', first_name='{self.first_name}')>"

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    grades = relationship("Grade", back_populates="course")
    
    def __repr__(self):
        return f"<Course(name='{self.name}')>"

class Grade(Base):
    __tablename__ = 'grades'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    score = Column(Integer, nullable=False)
    
    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")
    
    def __repr__(self):
        return f"<Grade(student_id={self.student_id}, course_id={self.course_id}, score={self.score})>"
