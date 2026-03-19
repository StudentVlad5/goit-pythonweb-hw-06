from sqlalchemy import func, desc
from db import session
from models import Student, Group, Teacher, Subject, Grade

# 1. Топ-5 студентів
def select_1():
    return session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .join(Grade).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()

# 2. Найкращий з предмета
def select_2(subject_name):
    return session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .join(Grade).join(Subject).filter(Subject.name == subject_name)\
        .group_by(Student.id).order_by(desc('avg_grade')).first()

# 3. Сер. бал у групах з предмета
def select_3(subject_name):
    return session.query(Group.name, func.round(func.avg(Grade.grade), 2))\
        .select_from(Group).join(Student).join(Grade).join(Subject)\
        .filter(Subject.name == subject_name)\
        .group_by(Group.id).all()

# 4. Сер. бал на потоці
def select_4():
    return session.query(func.round(func.avg(Grade.grade), 2)).scalar()

# 5. Курси викладача
def select_5(teacher_name):
    return session.query(Subject.name).join(Teacher)\
        .filter(Teacher.fullname == teacher_name).all()

# 6. Студенти в групі
def select_6(group_name):
    return session.query(Student.fullname).join(Group)\
        .filter(Group.name == group_name).all()

# 7. Оцінки групи з предмета
def select_7(group_name, subject_name):
    return session.query(Student.fullname, Grade.grade)\
        .select_from(Grade).join(Student).join(Group).join(Subject)\
        .filter(Group.name == group_name, Subject.name == subject_name).all()

# 8. Сер. бал викладача
def select_8(teacher_name):
    return session.query(func.round(func.avg(Grade.grade), 2))\
        .select_from(Grade).join(Subject).join(Teacher)\
        .filter(Teacher.fullname == teacher_name).scalar()

# 9. Список курсів, які відвідує певний студент.
def select_9(student_name):
    return session.query(Subject.name).distinct()\
        .join(Grade)\
        .join(Student)\
        .filter(Student.fullname == student_name).all()

# 10. Список курсів, які певному студенту читає певний викладач.
def select_10(student_name, teacher_name):
    return session.query(Subject.name).distinct()\
        .join(Grade)\
        .join(Student)\
        .join(Teacher)\
        .filter(Student.fullname == student_name, Teacher.fullname == teacher_name).all()

# 11. Сер. бал викладача для студента
def select_11(teacher_name, student_name):
    return session.query(func.round(func.avg(Grade.grade), 2))\
        .select_from(Grade)\
        .join(Subject).join(Teacher)\
        .join(Student)\
        .filter(Teacher.fullname == teacher_name, Student.fullname == student_name).scalar()

# 12. Останнє заняття
def select_12(group_name, subject_name):
    # Отримуємо дату останнього заняття
    last_date = session.query(func.max(Grade.grade_date))\
        .select_from(Grade).join(Student).join(Group).join(Subject)\
        .filter(Group.name == group_name, Subject.name == subject_name).scalar()
    
    if not last_date:
        return []

    return session.query(Student.fullname, Grade.grade)\
        .select_from(Grade).join(Student).join(Group).join(Subject)\
        .filter(Group.name == group_name, Subject.name == subject_name, Grade.grade_date == last_date).all()