def match_students(students, employers, vacancies):
    matches = {}
    remaining_vacancies = vacancies.copy()
    first_choice_counts = {position: 0 for position in vacancies}
    first_choice_students = {position: [] for position in vacancies}
    matched_students = set()  # Keep track of students who have been matched

    # Collect first choices and identify conflicts
    for student, preferences in students.items():
        first_choice = preferences[0]
        first_choice_counts[first_choice] += 1
        first_choice_students[first_choice].append(student)

    # Resolve conflicts using employer preferences
    for position, student_list in first_choice_students.items():
        if first_choice_counts[position] > vacancies[position]:
            # Sort students in conflict based on employer preference
            sorted_students = sorted(student_list, key=lambda x: employers[position].index(x) if x in employers[position] else float('inf'))
            for student in sorted_students[:vacancies[position]]:
                if student in employers[position]:
                    # Check if the employer has the student in their rankings
                    matches[student] = position
                    matched_students.add(student)
                    remaining_vacancies[position] -= 1
        else:
            for student in student_list:
                if student in employers[position]:
                    # Check if the employer has the student in their rankings
                    matches[student] = position
                    matched_students.add(student)
                    remaining_vacancies[position] -= 1

    # Assign remaining choices to students who were not matched in the first round
    for student, preferences in students.items():
        if student not in matched_students:
            for choice in preferences[1:]:  # Start from the second preference

                if remaining_vacancies.get(choice, 0) > 0 and student in employers.get(choice, []):
                    # Check if this choice is someone's first choice
                    first_choicers = [s for s in first_choice_students[choice] if s not in matched_students]
                    if not first_choicers or remaining_vacancies[choice] > len(first_choicers):
                        matches[student] = choice
                        matched_students.add(student)
                        remaining_vacancies[choice] -= 1
                        break

    # Mark any remaining students as unmatched
    for student in students:
        if student not in matched_students:
            matches[student] = "Unmatched"

    return matches


#example test
student_preferences = {
    'Alice': ['A', 'B', 'C', 'D', 'E'],
    'Bob': ['A', 'F', 'E', 'G', 'H'],
    'Charlie': ['B', 'E', 'D', 'F', 'A'],
    'Diana': ['C', 'B', 'A', 'H', 'I'],
    'Emily': ['D', 'C', 'H', 'I', 'J'],
    'Frank': ['E', 'D', 'G', 'B', 'J'],
    'Grace': ['F', 'A', 'I', 'J', 'C'],
    'Henry': ['G', 'F', 'B', 'E', 'D'],
    'Ian': ['H', 'G', 'J', 'A', 'F'],
    'Jack': ['I', 'H', 'G', 'D', 'B']
}

employer_preferences = {
    'A': ['Bob', 'Diana', 'Grace', 'Alice', 'Ian'],
    'B': ['Charlie', 'Henry', 'Jack', 'Diana', 'Alice'],
    'C': ['Diana', 'Emily', 'Grace', 'Frank', 'Charlie'],
    'D': ['Emily', 'Frank', 'Alice', 'Ian', 'Jack'],
    'E': ['Frank', 'Bob', 'Henry', 'Charlie', 'Alice'],
    'F': ['Grace', 'Henry', 'Ian', 'Charlie', 'Bob'],
    'G': ['Henry', 'Ian', 'Jack', 'Frank', 'Diana'],
    'H': ['Ian', 'Jack', 'Bob', 'Emily', 'Grace'],
    'I': ['Jack', 'Ian', 'Emily', 'Grace', 'Diana'],
    'J': ['Emily', 'Grace', 'Frank', 'Ian', 'Henry']
}

vacancies = {'A': 1, 'B': 1, 'C': 2, 'D': 1, 'E': 3, 'F': 1, 'G': 1, 'H': 2, 'I': 1, 'J': 1}

student_preferences_1 = {
    'Alice': ['A', 'B', 'C', 'D', 'E'],
    'Bob': ['A', 'F', 'E', 'G', 'H'],
    'Charlie': ['B', 'E', 'D', 'F', 'A'],
    'Diana': ['C', 'B', 'A', 'H', 'I'],
    'Emily': ['D', 'C', 'H', 'I', 'J'],
    'Frank': ['E', 'D', 'G', 'B', 'J'],
}

employer_preferences_1 = {
    'A': ['Bob', 'Diana', 'Grace', 'Alice', 'Isla'],
    'B': ['Charlie', 'Henry', 'Jack', 'Diana', 'Alice'],
    'C': ['Diana', 'Emily', 'Grace', 'Frank', 'Charlie'],
    'D': ['Emily', 'Frank', 'Alice', 'Isla', 'Jack'],
    'E': ['Frank', 'Bob', 'Henry', 'Charlie', 'Alice'],
    'F': ['Grace', 'Henry', 'Isla', 'Charlie', 'Bob'],
    'G': ['Henry', 'Isla', 'Jack', 'Frank', 'Diana'],
}

vacancies_1 = {'A': 1, 'B': 1, 'C': 1, 'D': 1, 'E': 1, 'F': 1, 'G': 1}





# Running the matching algorithm
matches = match_students(student_preferences, employer_preferences, vacancies)
for student, match in matches.items():
    print("")
    print(f"{student}: {match}")

