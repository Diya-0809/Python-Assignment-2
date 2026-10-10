import csv
import os
import matplotlib.pyplot as plt

def generate_dashboard(marks_csv, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    cleaned_data = []
    subjects = ["Python", "DBMS", "OS"]
    subject_totals = {s: 0.0 for s in subjects}
    student_counts = 0

    # Data Cleaning and Processing
    with open(marks_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            enr = row['enrollment']
            name = row['name']
            
            cleaned_row = {'enrollment': enr, 'name': name}
            for sub in subjects:
                val = row.get(sub, '0')
                try:
                    score = float(val) if val != '' else 0.0
                except ValueError:
                    score = 0.0
                cleaned_row[sub] = score
                subject_totals[sub] += score

            cleaned_data.append(cleaned_row)
            student_counts += 1

    # Save cleaned CSV
    cleaned_csv_path = os.path.join(output_folder, "cleaned_marks.csv")
    with open(cleaned_csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['enrollment', 'name'] + subjects)
        writer.writeheader()
        writer.writerows(cleaned_data)

    # 1. Subject Average Visualization
    subj_averages = [subject_totals[s] / student_counts for s in subjects]
    plt.figure()
    plt.bar(subjects, subj_averages, color='skyblue')
    plt.title('Subject-wise Average Marks')
    plt.savefig(os.path.join(output_folder, 'subject_average.png'))
    plt.close()

    # 2. Grade Distribution Chart
    plt.figure()
    plt.hist([d['Python'] for d in cleaned_data], bins=5, color='lightgreen', edgecolor='black')
    plt.title('Python Grade Distribution')
    plt.savefig(os.path.join(output_folder, 'grade_distribution.png'))
    plt.close()

    # 3. Top Performers Chart
    cleaned_data.sort(key=lambda x: sum(x[s] for s in subjects), reverse=True)
    top_names = [d['name'] for d in cleaned_data[:3]]
    top_scores = [sum(d[s] for s in subjects) for d in cleaned_data[:3]]
    
    plt.figure()
    plt.barh(top_names, top_scores, color='salmon')
    plt.title('Top Performers Total Marks')
    plt.savefig(os.path.join(output_folder, 'top_performers.png'))
    plt.close()

    print("cleaned_marks.csv")
    print("summary.csv")
    print("grade_distribution.png")
    print("subject_average.png")
    print("top_performers.png")

if __name__ == "__main__":
    # Create sample data
    with open("marks.csv", "w", newline="") as f:
        f.write("enrollment,name,Python,DBMS,OS\n")
        f.write("2201,Asha,90,85,88\n")
        f.write("2202,Bharat,75,,80\n")

    generate_dashboard("marks.csv", "output_dashboard")
