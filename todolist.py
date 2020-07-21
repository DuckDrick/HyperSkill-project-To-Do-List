from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)

Session = sessionmaker(bind = engine)
session = Session()

weekDays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


def print_tasks(tasks, dates=False, missed=False):
    if len(tasks) == 0:
        print("Nothing to do!" if not missed else "Nothing is missed!")
    else:
        for task in tasks:
            print(f'{task.id}. {task}{". {} {}".format(task.deadline.day, task.deadline.strftime("%b")) if dates else ""}')


def get_rows(tasks):
    if tasks == "all":
        return session.query(Table).all()
    elif tasks == "today":
        return session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    elif tasks == "week":
        print()
        tasks = []
        for days in range(7):
            find_day = datetime.today().date() + timedelta(days=days)
            tasks.append(session.query(Table).filter(Table.deadline == find_day).all())
    return tasks


def missed_tasks():
    tasks = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    print("\nMissed tasks:")
    print_tasks(tasks, dates=True, missed=True)


def add_task():
    task = input("Enter task\n")
    deadline = datetime.strptime(input("Enter deadline\n"), "%Y-%m-%d")
    new_row = Table(task = task, deadline = deadline)
    session.add(new_row)
    session.commit()
    print("The task has been added!\n")


def delete_task():
    print("Chose the number of the task you want to delete:")
    print_tasks(get_rows("all"), dates=True)
    delete = int(input())
    to_delete = session.query(Table).filter(Table.id == delete).all()
    if not len(to_delete):
        print("There is no task with that number!\n")
    else:
        session.delete(to_delete[0])
        session.commit()
        print("The task has been deleted!\n")


selection = -1
while selection != 0:
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    selection = int(input())
    if selection == 1:
        print("\nToday {} {}:".format(datetime.today().day, datetime.today().strftime("%b")))
        print_tasks(get_rows("today"))
        print()
    elif selection == 2:
        rows = get_rows("week")
        day = datetime.today().date()
        for i in range(7):
            print(f'{weekDays[day.weekday()]} {day.day} {day.strftime("%b")}:')
            print_tasks(rows[i])
            print()
            day = day + timedelta(days=1)
    elif selection == 3:
        print("\nAll tasks:")
        print_tasks(get_rows("all"), True)
        print()
    elif selection == 4:
        missed_tasks()
    elif selection == 5:
        add_task()
    elif selection == 6:
        delete_task();

print("\nBye!")


