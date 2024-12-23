
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=False)

engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

def create_task(name, description):
    task = Task(name=name, description=description)
    session.add(task)
    session.commit()
    print(f"Task '{name}' created successfully!")

def read_tasks():
    tasks = session.query(Task).all()
    for task in tasks:
        status = "Completed" if task.status else "Pending"
        print(f"ID: {task.id}, Name: {task.name}, Description: {task.description}, Status: {status}")

def update_task_status(task_id, status):
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = status
        session.commit()
        print(f"Task '{task.name}' updated successfully!")
    else:
        print("Task not found.")

def delete_task(task_id):
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        session.delete(task)
        session.commit()
        print(f"Task '{task.name}' deleted successfully!")
    else:
        print("Task not found.")

def main():
    while True:
        print("\nChoose an action:")
        print("1. Create task")
        print("2. Read tasks")
        print("3. Update task status")
        print("4. Delete task")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter task name: ")
            description = input("Enter task description: ")
            create_task(name, description)
        elif choice == "2":
            read_tasks()
        elif choice == "3":
            task_id = int(input("Enter task ID: "))
            status = input("Enter new status (completed/pending): ").lower() == "completed"
            update_task_status(task_id, status)
        elif choice == "4":
            task_id = int(input("Enter task ID to delete: "))
            delete_task(task_id)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
