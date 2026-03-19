from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    group = relationship("Group", back_populates="students")

Group.students = relationship("Student", order_by=Student.id, back_populates="group")

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher = relationship("Teacher", back_populates="subjects")

Teacher.subjects = relationship("Subject", order_by=Subject.id, back_populates="teacher")

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, CheckConstraint('grade >= 0 AND grade <= 100'), nullable=False)
    grade_date = Column(DateTime, default=datetime.now)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'))
    
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

Student.grades = relationship("Grade", order_by=Grade.grade_date, back_populates="student")
Subject.grades = relationship("Grade", order_by=Grade.grade_date, back_populates="subject")