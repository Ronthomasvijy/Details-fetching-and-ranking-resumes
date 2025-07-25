import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import pdfplumber
import re
import spacy
import re
import pdfplumber
from rapidfuzz import fuzz
import os
import re


base_path = r"C:\Users\ron61\resumes"
nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

myresume=extract_text_from_pdf(r"C:\Users\ron61\Ron Thomas Vijy resume.pdf")
# print(myresume)
def jd(job_description):
    jd=job_description.lower()
    text = jd.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if w not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(w) for w in tokens]
    job_des=' '.join(tokens)
    # print("Preprocessed JD:\n",final)
    return job_des


def resume(job_resume):
    jr=job_resume.lower()
    text = jr.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if w not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(w) for w in tokens]
    job_res=' '.join(tokens)
    # print("Preprocessed JD:\n",final)
    return job_res


def tfidvectorizer_score_generator(job_description,base_path):
    resume_filenames=[]
    jd_list=[jd(job_description)]
    corpus=[]
    corpus.extend(jd_list)
    for file_name in os.listdir(base_path):
        if file_name.lower().endswith('.pdf'):
            resume_filenames.append(file_name)
            file_path = os.path.join(base_path, file_name)
            myresume=extract_text_from_pdf(file_path)
            my_cleaned_resume=resume(myresume)
            my_cleaned_resume_list=[my_cleaned_resume]
            corpus.extend(my_cleaned_resume_list)
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(corpus)
    print("TF-IDF Shape:", vectors.shape)
    similarities = cosine_similarity(vectors[0:1],vectors[1:])[0]
    resume_similarity_dict = {filename: float(score) for filename, score in zip(resume_filenames, similarities)}
    return resume_similarity_dict


def sentencebert_score_generator(job_description, base_path):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    resume_filenames = []
    resume_texts = []
    for file_name in os.listdir(base_path):
        if file_name.lower().endswith('.pdf'):
            file_path = os.path.join(base_path, file_name)
            resume_text = extract_text_from_pdf(file_path)
            if resume_text.strip():
                resume_filenames.append(file_name)
                resume_texts.append(resume_text)

    embeddings = model.encode([job_description] + resume_texts, convert_to_tensor=True)
    similarities = util.cos_sim(embeddings[0], embeddings[1:])[0]
    resume_similarity_dict = {
        filename: float(score)
        for filename, score in zip(resume_filenames, similarities)
    }
    return resume_similarity_dict




try:
    with open(r"C:\Users\ron61\OneDrive\Desktop\jd.txt", 'r', encoding='utf-8') as file:
        job_decription = file.read() # Reads the entire content as a single string

    print("job description:")
    print(job_decription)
    idvec_score=tfidvectorizer_score_generator(job_decription,base_path)
    bert_score=sentencebert_score_generator(job_decription,base_path)
    print(idvec_score)
    print(bert_score)
except FileNotFoundError:
    print(f"Error: The file was not found.")
except Exception as e:
    print(f"An error occurred: {e}")





# read job description fronm txt file