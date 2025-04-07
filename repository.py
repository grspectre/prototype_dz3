import csv
from sqlalchemy import func
from model import create_engine, sessionmaker, Faculty, Student, Grade, Course, Base

class StudentRepository:
    def __init__(self, db_url="sqlite:///students.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def import_from_csv(self, file_path):
        """Импорт данных из CSV файла"""
        session = self.Session()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # Получаем или создаем факультет
                    faculty = session.query(Faculty).filter_by(name=row['Факультет']).first()
                    if not faculty:
                        faculty = Faculty(name=row['Факультет'])
                        session.add(faculty)
                        session.flush()  # Чтобы получить id факультета
                    
                    # Получаем или создаем студента
                    student = session.query(Student).filter_by(
                        last_name=row['Фамилия'], 
                        first_name=row['Имя'],
                        faculty_id=faculty.id
                    ).first()
                    
                    if not student:
                        student = Student(
                            last_name=row['Фамилия'],
                            first_name=row['Имя'],
                            faculty_id=faculty.id
                        )
                        session.add(student)
                        session.flush()  # Чтобы получить id студента
                    
                    # Получаем или создаем курс
                    course = session.query(Course).filter_by(name=row['Курс']).first()
                    if not course:
                        course = Course(name=row['Курс'])
                        session.add(course)
                        session.flush()  # Чтобы получить id курса
                    
                    # Проверяем, есть ли уже такая оценка
                    existing_grade = session.query(Grade).filter_by(
                        student_id=student.id,
                        course_id=course.id
                    ).first()
                    
                    if not existing_grade:
                        # Добавляем оценку
                        grade = Grade(
                            student_id=student.id,
                            course_id=course.id,
                            score=int(row['Оценка'])
                        )
                        session.add(grade)
            
            session.commit()
            print("Данные успешно импортированы из CSV")
        except Exception as e:
            session.rollback()
            print(f"Ошибка при импорте данных: {str(e)}")
        finally:
            session.close()
    
    def get_students_by_faculty(self, faculty_name):
        """Получение списка студентов по названию факультета"""
        session = self.Session()
        try:
            students = session.query(Student).join(Faculty).filter(
                Faculty.name == faculty_name
            ).all()
            
            result = []
            for student in students:
                result.append({
                    'id': student.id,
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'faculty': student.faculty.name
                })
            
            return result
        finally:
            session.close()
    
    def get_unique_courses(self):
        """Получение списка уникальных курсов"""
        session = self.Session()
        try:
            courses = session.query(Course).all()
            return [{'id': course.id, 'name': course.name} for course in courses]
        finally:
            session.close()
    
    def get_average_score_by_faculty(self, faculty_name):
        """Получение среднего балла по факультету"""
        session = self.Session()
        try:
            avg_score = session.query(func.avg(Grade.score)).join(
                Student, Student.id == Grade.student_id
            ).join(
                Faculty, Faculty.id == Student.faculty_id
            ).filter(
                Faculty.name == faculty_name
            ).scalar()
            
            return avg_score
        finally:
            session.close()
    
    def get_students_with_low_score(self, course_name, max_score=30):
        """Получение списка студентов по выбранному курсу с оценкой ниже указанного значения"""
        session = self.Session()
        try:
            students = session.query(Student).join(
                Grade, Grade.student_id == Student.id
            ).join(
                Course, Course.id == Grade.course_id
            ).filter(
                Course.name == course_name,
                Grade.score < max_score
            ).all()
            
            result = []
            for student in students:
                # Найдем оценку для этого студента по этому курсу
                score = session.query(Grade.score).filter(
                    Grade.student_id == student.id,
                    Grade.course_id == session.query(Course.id).filter(Course.name == course_name).scalar()
                ).scalar()
                
                result.append({
                    'id': student.id,
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'faculty': student.faculty.name,
                    'course': course_name,
                    'score': score
                })
            
            return result
        finally:
            session.close()
