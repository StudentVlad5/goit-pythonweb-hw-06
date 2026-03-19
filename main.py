import sys
from db import session
from models import Teacher, Group, Student, Subject, Grade

# Конфігурація моделей: назва, клас, основне поле для відображення
MODELS = {
    '1': ('Teacher', Teacher, 'fullname'),
    '2': ('Group', Group, 'name'),
    '3': ('Student', Student, 'fullname'),
    '4': ('Subject', Subject, 'name'),
    '5': ('Grade', Grade, 'grade')
}

def get_item_by_number(model_class, attr_name, title="запис"):
    items = session.query(model_class).all()
    if not items:
        print(f"❌ У базі немає жодного запису {model_class.__name__}")
        return None
        
    print(f"\n--- Оберіть {title} ---")
    for i, item in enumerate(items, 1):
        val = getattr(item, attr_name)
        print(f"{i}. {val} (ID: {item.id})")
    
    while True:
        try:
            choice = int(input(f"Введіть номер (1-{len(items)}): "))
            if 1 <= choice <= len(items):
                return items[choice - 1]
        except ValueError:
            print("Будь ласка, введіть число.")

def handle_create(model_name, model_class):
    print(f"\n--- Створення {model_name} ---")
    new_obj = None

    if model_name == 'Teacher':
        name = input("ПІБ викладача: ")
        new_obj = Teacher(fullname=name)
        
    elif model_name == 'Group':
        name = input("Назва групи: ")
        new_obj = Group(name=name)
        
    elif model_name == 'Student':
        name = input("ПІБ студента: ")
        group = get_item_by_number(Group, 'name', "групу")
        if group: new_obj = Student(fullname=name, group_id=group.id)
        
    elif model_name == 'Subject':
        name = input("Назва предмета: ")
        teacher = get_item_by_number(Teacher, 'fullname', "викладача")
        if teacher: new_obj = Subject(name=name, teacher_id=teacher.id)
        
    elif model_name == 'Grade':
        student = get_item_by_number(Student, 'fullname', "студента")
        subject = get_item_by_number(Subject, 'name', "предмет")
        val = int(input("Введіть оцінку (0-100): "))
        if student and subject:
            new_obj = Grade(grade=val, student_id=student.id, subject_id=subject.id)

    if new_obj:
        session.add(new_obj)
        session.commit()
        print("✅ Успішно створено!")
    else:
        print("⚠️ Створення скасовано (недостатньо даних).")

def handle_edit(model_name, model_class, attr_name):
    print(f"\n--- Редагування {model_name} ---")
    item = get_item_by_number(model_class, attr_name, model_name)
    if not item: return

    if model_name == 'Grade':
        new_val = int(input(f"Введіть нову оцінку (зараз {item.grade}): "))
        item.grade = new_val
    else:
        new_val = input(f"Введіть нове значення для {attr_name} (зараз '{getattr(item, attr_name)}'): ")
        setattr(item, attr_name, new_val)
    
    session.commit()
    print("🔄 Оновлено!")

def handle_delete(model_name, model_class, attr_name):
    print(f"\n--- Видалення {model_name} ---")
    item = get_item_by_number(model_class, attr_name, model_name)
    if not item: return

    confirm = input(f"❗ Ви впевнені, що хочете видалити '{getattr(item, attr_name)}'? (y/n): ")
    if confirm.lower() == 'y':
        session.delete(item)
        session.commit()
        print("🗑️ Видалено каскадно (пов'язані дані також стерто).")

def main():
    while True:
        print("\n" + "="*30)
        print("  ІНТЕРАКТИВНИЙ CRUD МЕНЕДЖЕР")
        print("="*30)
        print("1. Вчителі | 2. Групи | 3. Студенти | 4. Предмети | 5. Оцінки | 0. Вихід")
        m_choice = input("Оберіть модель: ")
        
        if m_choice == '0': break
        if m_choice not in MODELS:
            print("❌ Невірний вибір моделі.")
            continue
        
        m_name, m_class, m_attr = MODELS[m_choice]
        
        print(f"\nДія для {m_name}:")
        print("1. Список | 2. Створити | 3. Редагувати | 4. Видалити")
        action = input("Ваш вибір: ")

        try:
            if action == '1':
                items = session.query(m_class).all()
                print(f"\n--- Список {m_name} ---")
                for it in items:
                    print(f"- {getattr(it, m_attr)} (ID: {it.id})")
            elif action == '2':
                handle_create(m_name, m_class)
            elif action == '3':
                handle_edit(m_name, m_class, m_attr)
            elif action == '4':
                handle_delete(m_name, m_class, m_attr)
            else:
                print("❌ Невідома дія.")
        except Exception as e:
            print(f"❌ Помилка: {e}")
            session.rollback()

if __name__ == "__main__":
    main()