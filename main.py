import sqlite3
from datetime import datetime

# Подключение к базе данных
db = sqlite3.connect('tasks.db')
c = db.cursor()

# Функция для проверки формата даты
def validate_deadline(deadline):
    try:
        datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

# Добавление приоритетов по умолчанию
def add_default_priorities():
    c.execute("SELECT COUNT(*) FROM Priorities")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO Priorities (priority_level) VALUES (?)",
                      [("Низкий",), ("Средний",), ("Высокий",)])
        db.commit()

# Функция для показа приоритетов
def show_priorities():
    c.execute("SELECT * FROM Priorities")
    priorities = c.fetchall()
    print("\nДоступные приоритеты:")
    for priority in priorities:
        print(f"{priority[0]}. {priority[1]}")

# Функция для показа задач
def show_task():
    c.execute("SELECT * FROM Tasks")
    tasks = c.fetchall()
    print("Задачи выводятся в порядке: Приоритет, задача, готовность, дедлайн")
    for task in tasks:
        print(f"Приоритет: {task[3]}, Задача: {task[4]}, Готовность: {task[5]}, Дедлайн: {task[6]}")

# Функция для добавления задачи
def add_task():
    task = input("Введите название задачи: ").strip()
    if not task:
        print("Название задачи не может быть пустым.")
        return

    deadline = input("Введите дедлайн задачи (в формате YYYY-MM-DD hh:mm:ss): ").strip()
    if not validate_deadline(deadline):
        print("Ошибка: некорректный формат даты.")
        return

    show_priorities()
    try:
        priority = int(input("Введите номер приоритета: ").strip())
        if priority not in [1, 2, 3]:
            raise ValueError("Некорректный приоритет.")
    except ValueError as e:
        print(f"Ошибка: {e}")
        return

    c.execute("INSERT INTO Tasks (task, deadline, id_priority, execution) VALUES (?, ?, ?, ?)",
              (task, deadline, priority, "не выполнено"))
    db.commit()
    print(f"Задача '{task}' добавлена успешно.")

# Функция для изменения задачи
def change_task():
    show_task()
    try:
        tasks_id = int(input("Введите ID задачи, которую хотите изменить: "))
        c.execute("SELECT * FROM Tasks WHERE id_tasks = ?", (tasks_id,))
        task = c.fetchone()
        if not task:
            print("Задача с таким ID не найдена.")
            return
    except ValueError:
        print("Ошибка: введите корректный ID.")
        return

    print(f"\nТекущие данные задачи (ID: {tasks_id}):")
    print(f"Приоритет: {task[3]}, Задача: {task[4]}, Готовность: {task[5]}, Дедлайн: {task[6]}")

    new_priority = input("Введите новый приоритет: ").strip() or task[3]
    new_name = input("Введите новое название: ").strip() or task[4]
    new_execution = input("Введите готовность: ").strip() or task[5]
    new_deadline = input("Введите новый дедлайн: ").strip() or task[6]

    c.execute("""
    UPDATE Tasks
    SET id_priority = ?, task = ?, execution = ?, deadline = ?
    WHERE id_tasks = ?
    """, (new_priority, new_name, new_execution, new_deadline, tasks_id))
    db.commit()
    print("Задача успешно обновлена.")

# Функция для удаления задачи
def delete_task():
    show_task()
    try:
        task_id = int(input("Введите ID задачи, которую хотите удалить: "))
        c.execute("DELETE FROM Tasks WHERE id_tasks = ?", (task_id,))
        if c.rowcount == 0:
            print("Задача с таким ID не найдена.")
        else:
            db.commit()
            print("Задача успешно удалена.")
    except ValueError:
        print("Ошибка: введите корректный ID.")

# Главное меню
def main():
    add_default_priorities()
    while True:
        print("\n1. Показать задачи")
        print("2. Добавить задачу")
        print("3. Изменить задачу")
        print("4. Удалить задачу")
        print("5. Выйти")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            show_task()
        elif choice == "2":
            add_task()
        elif choice == "3":
            change_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("До свидания!")
            break
        else:
            print("Ошибка: некорректный ввод.")

if __name__ == "__main__":
    main()
    db.commit()
    db.close()
