import random
from faker import Faker
from db import session, engine
from models import Group, Teacher, Subject, Student, Grade
from models import Base

fake = Faker()
Base.metadata.create_all(bind=engine)

def fill_data():
    # 1. Створюємо групи
    groups = [Group(name=f"Group {i}") for i in ['AA-101', 'AB-101', 'AC-102']]
    session.add_all(groups)
    
    # 2. Створюємо викладачів (3-5 осіб)
    teachers = [Teacher(fullname=fake.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit() # Зберігаємо, щоб отримати ID для зв'язків

    # 3. Створюємо предмети (5-8 предметів)
    subject_names = ["Math", "Physics", "History", "Programming", "Biology", "English"]
    subjects = []
    for s_name in subject_names:
        subjects.append(Subject(name=s_name, teacher=random.choice(teachers)))
    session.add_all(subjects)
    
    # 4. Створюємо студентів (30-50 осіб)
    students = []
    for _ in range(40):
        student = Student(fullname=fake.name(), group=random.choice(groups))
        students.append(student)
    session.add_all(students)
    session.commit()

    # 5. Створюємо оцінки (до 20 на кожного студента)
    # Беремо всіх студентів та предмети з бази
    for student in students:
        for _ in range(random.randint(10, 20)):
            grade = Grade(
                grade=random.randint(40, 100),
                grade_date=fake.date_this_year(),
                student=student,
                subject=random.choice(subjects)
            )
            session.add(grade)
    
    session.commit()
    print(" База даних успішно заповнена випадковими даними!")

if __name__ == "__main__":
    fill_data()