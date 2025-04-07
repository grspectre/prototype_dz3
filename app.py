from repository import StudentRepository


if __name__ == "__main__":
    # Создаем репозиторий для работы с данными
    repo = StudentRepository()
    
    # Импортируем данные из CSV
    repo.import_from_csv("students.csv")
    
    # Примеры использования методов    
    # 1. Получение списка студентов по факультету
    students = repo.get_students_by_faculty("ФТФ")
    print("\nСтуденты факультета ФТФ:")
    for student in students:
        print(f"{student['last_name']} {student['first_name']}")
    
    # 2. Получение списка уникальных курсов
    courses = repo.get_unique_courses()
    print("\nСписок всех курсов:")
    for course in courses:
        print(course['name'])
    
    # 3. Получение среднего балла по факультету
    avg_score = repo.get_average_score_by_faculty("АВТФ")
    print(f"\nСредний балл на факультете АВТФ: {avg_score:.2f}")
    
    # 4. Получение студентов с низкими оценками по курсу
    low_performers = repo.get_students_with_low_score("Мат. Анализ")
    print("\nСтуденты с оценкой ниже 30 по курсу 'Мат. Анализ':")
    for student in low_performers:
        print(f"{student['last_name']} {student['first_name']} - {student['score']} баллов")
