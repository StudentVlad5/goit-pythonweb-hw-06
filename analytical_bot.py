import sys
import my_select
from db import session
from models import Student, Group, Teacher, Subject

def get_choice(items, attr='fullname', title="об'єкт"):
    if not items:
        print(f"Помилка: {title} не знайдено в базі.")
        return None
        
    for i, item in enumerate(items, 1):
        name = getattr(item, attr)
        print(f"{i}. {name}")
    
    while True:
        try:
            idx = int(input(f"\nОберіть номер {title}: ")) - 1
            if 0 <= idx < len(items):
                return items[idx]
            print("Невірний номер.")
        except ValueError:
            print("Введіть число.")

def get_teacher(): return get_choice(session.query(Teacher).all(), title="викладача")
def get_subject(): return get_choice(session.query(Subject).all(), attr='name', title="предмет")
def get_group():   return get_choice(session.query(Group).all(), attr='name', title="групу")
def get_student(): return get_choice(session.query(Student).all(), title="студента")

# --- ГОЛОВНИЙ ЦИКЛ ---

def run():
    while True:
        print("\n" + "="*60)
        print(" СИСТЕМА ЗВІТНОСТІ УНІВЕРСИТЕТУ (1-12)")
        print("="*60)
        print("1.  ТОП-5 студентів (загальний рейтинг)")
        print("2.  Найкращий студент з ПРЕДМЕТА")
        print("3.  Сер. бал ГРУП з ПРЕДМЕТА")
        print("4.  Загальний сер. бал по всьому потоку")
        print("5.  Які курси читає ВИКЛАДАЧ")
        print("6.  Список студентів ГРУПИ")
        print("7.  Оцінки ГРУПИ з ПРЕДМЕТА")
        print("8.  Сер. бал, який ставить ВИКЛАДАЧ")
        print("9.  Курси, які відвідує СТУДЕНТ")
        print("10. Курси СТУДЕНТА від конкретного ВИКЛАДАЧА")
        print("-" * 20 + " ДОДАТКОВІ " + "-" * 23)
        print("11. Сер. бал, який ВИКЛАДАЧ ставить СТУДЕНТУ")
        print("12. Оцінки ГРУПИ з ПРЕДМЕТА на ОСТАННЬОМУ занятті")
        print("0.  Вихід")
        
        choice = input("\nВведіть номер звіту: ")

        if choice == '1':
            print("\nРезультат:", my_select.select_1())

        elif choice == '2':
            s = get_subject()
            if s: print(f"\nНайкращий у '{s.name}':", my_select.select_2(s.name))

        elif choice == '3':
            s = get_subject()
            if s: print(f"\nСер. бали по групах ({s.name}):", my_select.select_3(s.name))

        elif choice == '4':
            print("\nСередній бал потоку:", my_select.select_4())

        elif choice == '5':
            t = get_teacher()
            if t: print(f"\nКурси викладача {t.fullname}:", my_select.select_5(t.fullname))

        elif choice == '6':
            g = get_group()
            if g: print(f"\nСтуденти групи {g.name}:", my_select.select_6(g.name))

        elif choice == '7':
            g = get_group(); s = get_subject()
            if g and s: print(f"\nОцінки ({g.name} -> {s.name}):", my_select.select_7(g.name, s.name))

        elif choice == '8':
            t = get_teacher()
            if t: print(f"\nСер. бал викладача {t.fullname}:", my_select.select_8(t.fullname))

        elif choice == '9':
            st = get_student()
            if st: print(f"\nКурси студента {st.fullname}:", my_select.select_9(st.fullname))

        elif choice == '10':
            st = get_student(); t = get_teacher()
            if st and t: print(f"\nКурси {st.fullname} у {t.fullname}:", my_select.select_10(st.fullname, t.fullname))

        elif choice == '11':
            t = get_teacher(); st = get_student()
            if t and st: print(f"\nСер. бал ({t.fullname} -> {st.fullname}):", my_select.select_11(t.fullname, st.fullname))

        elif choice == '12':
            g = get_group(); s = get_subject()
            if g and s: print(f"\nОстаннє заняття ({g.name} -> {s.name}):", my_select.select_12(g.name, s.name))

        elif choice == '0':
            print("До побачення!")
            break
        else:
            print("Помилка: Оберіть число від 0 до 12.")

if __name__ == "__main__":
    run()