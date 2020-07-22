from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return "{} {} {}".format(self.id, self.task, self.deadline)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_task():
    print("Enter task")
    new_task = input()
    print("Enter deadline")
    task_deadline = input()
    task_deadline_format = datetime.strptime(task_deadline,'%Y-%m-%d')
    new_row = Table(task=new_task, deadline = task_deadline_format)
    session.add(new_row)
    session.commit()
    print("The task has been added!")
    print()

def today_task(tday):
    rows = session.query(Table).filter(Table.deadline == tday.date()).all()
    print(tday.strftime("Today %d %b:"))
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for num, row in enumerate(rows, start=1):
            print('{}. {}'.format(num, row.task))
    print()

def week_task(tday):
    for day_ in [tday.date() + timedelta(days=i) for i in range(7)]:
        rows = session.query(Table).filter(Table.deadline == day_).all()
        print("{} {} {}:".format(day_.strftime('%A'), day_.day, day_.strftime('%b')))
        if len(rows) == 0:
            print("Nothing to do!")
            print()
        else:
            for num, row in enumerate(rows, start=1):
                print('{}. {}'.format(num, row.task))
        print()

def all_task():
    print("All tasks:")
    rows = session.query(Table).all()
    for num, row in enumerate(rows, start = 1):
        print('{}. {}. {}'.format(num, row.task, row.deadline.strftime('%d %b')))
    print()

def missed_task(tday):
    print("Missed tasks:")
    rows = session.query(Table).filter(Table.deadline < tday.date()).order_by(Table.deadline).all()
    if len(rows) == 0:
        print("Nothing is missed!")
    else:
        for num, row in enumerate(rows, start=1):
                print('{}. {}. {}'.format(num, row.task, row.deadline.strftime('%d %b')))
    print()

def delete_task():
    rows = session.query(Table).order_by(Table.deadline).all()
    print("Chose the number of the task you want to delete:")
    for num, row in enumerate(rows, start = 1):
        print('{}. {}. {}'.format(num, row.task, row.deadline.strftime('%d %b')))
    choice = int(input()) + 1
    session.delete(rows[choice])
    session.commit()
    print("The task has been deleted!")
    print()

def todo_options():
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")

def todo_app():
    tday = datetime.now()
    while True:
        todo_options()
        choice = int(input())
        print()
        if choice == 1:
            today_task(tday)
        elif choice == 2:
            week_task(tday)
        elif choice == 3:
            all_task()
        elif choice == 4:
            missed_task(tday)
        elif choice == 5:
            add_task()
        elif choice == 6:
            delete_task()
        elif choice == 0:
            print("Bye!")
            break

todo_app()
