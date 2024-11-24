
import matplotlib.pyplot as plt
from matplotlib.font_manager import weight_dict
import os


# Helper functions to load data
def load_students(file_path):
    students = {}
    with open(file_path, 'r') as file:
        for line in file:
            student_id = line[:3].strip()  # Extract first 3 characters
            name = line[3:].strip()
            students[name] = int(student_id)
    return students

def load_assignments(file_path):
    assignments = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines
        for i in range(0, len(lines), 3):  # Process in chunks of 3 lines
            if i + 2 < len(lines):  # Ensure there are enough lines to form a complete assignment entry
                name = lines[i].strip()  # Assignment name
                assignment_id = int(lines[i + 1].strip())  # Assignment ID
                points = int(lines[i + 2].strip())  # Points
                assignments[name] = {"id": assignment_id, "points": points}
    return assignments


def load_submissions(directory_path):
    submissions = []
    for filename in os.listdir(directory_path):
        # Process only .txt files
        if filename.endswith(".txt"):
            # Extract assignment ID from the filename
            try:
                assignment_id = int(filename.split('.')[0])  # Remove .txt and get the numeric part
            except ValueError:
                continue  # Skip files that don't follow the numeric naming pattern

            # Read the file contents
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                for line in file:
                    try:
                        student_id, percent = map(float, line.strip().split())  # Split and convert data
                        submissions.append({
                            "assignment_id": assignment_id,
                            "student_id": int(student_id),
                            "percent": percent
                        })
                    except ValueError:
                        continue  # Skip invalid lines
    return submissions


# Function to calculate a student's grade
def calculate_student_grade(name, students, assignments, submissions):
    if name not in students:
        return None
    student_id = students[name]
    total_points_earned = 0
    total_points = sum(assignment["points"] for assignment in assignments.values())
    for submission in submissions:
        if submission["student_id"] == student_id:
            assignment_id = submission["assignment_id"]
            for assignment in assignments.values():
                if assignment["id"] == assignment_id:
                    total_points_earned += (submission["percent"] / 100) * assignment["points"]
                    break
    return round((total_points_earned / total_points) * 100)


# Function to calculate assignment statistics
def get_assignment_statistics(name, assignments, submissions):
    if name not in assignments:
        return None
    assignment_id = assignments[name]["id"]
    scores = [submission["percent"] for submission in submissions if submission["assignment_id"] == assignment_id]
    if not scores:
        return {"min": 0, "max": 0, "average": 0}  # Or handle as None
    return {"min": min(scores), "max": max(scores), "average": sum(scores) / len(scores)}

# Function to generate assignment histogram
def plot_assignment_histogram(name, assignments, submissions):
    if name not in assignments:
        return False
    assignment_id = assignments[name]["id"]
    scores = [submission["percent"] for submission in submissions if submission["assignment_id"] == assignment_id]
    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"Histogram for {name}")
    plt.xlabel("Percentage")
    plt.ylabel("Number of Students")
    plt.show()
    return True


# Main program
def main():
    students = load_students('data/students.txt')
    assignments = load_assignments('data/assignments.txt')
    submissions = load_submissions('data/submissions')

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    choice = input("Enter your selection: ")

    if choice == "1":
        name = input("What is the student's name: ")
        grade = calculate_student_grade(name, students, assignments, submissions)
        if grade is None:
            print("Student not found")
        else:
            print(f"{name}'s grade: {grade}%")
    elif choice == "2":
        name = input("What is the assignment name: ")
        stats = get_assignment_statistics(name, assignments, submissions)
        if stats is None:
            print("Assignment not found")
        else:
            print(f"{name} Statistics: Min={stats['min']}%, Max={stats['max']}%, Average={stats['average']:.2f}%")
    elif choice == "3":
        name = input("What is the assignment name: ")
        if not plot_assignment_histogram(name, assignments, submissions):
            print("Assignment not found")


if __name__ == "__main__":
    main()
