import csv
from resume_comparator import tfidvectorizer_score_generator, sentencebert_score_generator
from data_extracter import dictionary_of_details
base_path = r"C:\Users\ron61\resumes"
try:
    with open(r"C:\Users\ron61\OneDrive\Desktop\jd.txt", 'r', encoding='utf-8') as file:
        job_decription = file.read()  # Reads the entire content as a single string

    print("job description:")
    print(job_decription)
    idvec_score = tfidvectorizer_score_generator(job_decription, base_path)
    bert_score = sentencebert_score_generator(job_decription, base_path)
    print(idvec_score)
    print(bert_score)
    for i, j in idvec_score.items():
        print(i, "        ", j)
    print("\n-----\n")
    for j, i in bert_score.items():
        print(j, "         ", i)
    print("\n---------\n")
except FileNotFoundError:
    print(f"Error: The file was not found.")
except Exception as e:
    print(f"An error occurred: {e}")


final_detais = dictionary_of_details(base_path)
for k, l in final_detais.items():
    print(k, "         ", l)

output_csv_path = r"C:\resume_classifier\data_cleaned.csv"
header = ["filename", "tfidf_score", "bert_score", "average_score",
          "name", "phone", "email", "place"]

all_filenames = set(idvec_score.keys()) | set(
    bert_score.keys()) | set(final_detais.keys())

rows = []


for filename in all_filenames:
    details = final_detais.get(filename, ["", "", "", ""])
    id_score = idvec_score.get(filename)
    bert_sc = bert_score.get(filename)


    if id_score is not None and bert_sc is not None:
        avg_score = round(((float(id_score) + float(bert_sc)) / 2) * 100, 2)
    else:
        avg_score = ""

    row = {
        "filename": filename,
        "tfidf_score": id_score if id_score is not None else "",
        "bert_score": bert_sc if bert_sc is not None else "",
        "average_score": avg_score,
        "name": details[0],
        "email": details[1],
        "phone": details[2],
        "place": details[3]
    }

    rows.append(row)

rows.sort(key=lambda x: x["average_score"] if x["average_score"] != "" else -1, reverse=True)

with open(output_csv_path, mode="w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV file created with rows sorted by average score: {output_csv_path}")