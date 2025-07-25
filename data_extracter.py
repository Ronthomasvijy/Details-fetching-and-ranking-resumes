import re
import pdfplumber
from rapidfuzz import fuzz
import os
import re
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




def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

def extract_email(text):
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else "Email not found"


def extract_phone(text):
    phone_pattern = r'(\+91[\s\-]?|)(\d{5})[\s\-]?(\d{5})'
    matches = re.findall(phone_pattern, text)
    
    # Combine groups and return full number
    phones = [''.join(match) for match in matches]
    return phones[0] if phones else "Phone number not found"

def extract_name(email_address,text):
    email_address1=email_address[:email_address.find('@')]
    email_address2="".join(c for c in email_address1 if c.isalpha())
    # print(email_address2)  
    # print(text)
    lines=text.split('\n')
    high_score=0
    probable_name=""
    lin=0
    line_number=0
    for i in lines:
        lin+=1
        score = fuzz.partial_ratio(email_address2.lower(), i.lower())
        if score>high_score:
            if ' ' in i and len(i)<20:
                high_score=score
                probable_name=i
                line_number=lin
    return probable_name,line_number

def extract_district(text):
    district_names=["kasaragod","kannur","calicut","kozhikode","wayanad","malappuram","palakkad","palghat","thrissur","ernakulam","kochi","cochin","idukki","kottayam","kollam","pathanamthitta","kollam","trivandrum","thiruvananthapuram"]
    lines=text.split('\n')
    district_dict={}
    c=1
    for i in lines:
        c+=1
        ilower=i.lower()
        # print(ilower)
        for d in district_names:
            if d in district_dict.keys():
                continue
            if d in ilower:
                # print("hi")
                district_dict[d]=c
        # district_dict[c]=dis
    return district_dict

def approx_place_identification(linenumber,dict1):
    k=250
    dis = "Unknown"
    for key,value in dict1.items():
        distance=abs(value-linenumber)
        if distance<k:
            k=distance
            dis=key
    if k>30:
        dis="unknown"
    return dis
                
        
base_path = r"C:\Users\ron61\resumes"


# # base_path = r"C:\Users\ron61\resumes"
# resume = input("Enter filename: ")
# file_path = os.path.join(base_path, resume)
# print(f"\nExtracting from: {resume}")
# print("\n")
# resume_text = extract_text_from_pdf(file_path)
# # print(resume_text[:100])
# print("\n")
# email = extract_email(resume_text)
# phone = extract_phone(resume_text)
# name,linenumber = extract_name(email,resume_text)
# dict1=extract_district(resume_text)
# district=approx_place_identification(linenumber,dict1)
# print("Email:", email)
# print("Phone:", phone)
# print("Name:", name," ",linenumber)
# print("---",dict1,"---")
# print("place :",district)
# print("\n",'-'*10,"\n")

def dictionary_of_details(base_path):
    file_names=[]
    list_of_listdetails=[]
    for file_name in os.listdir(base_path):
        list_of_details=[]
        if file_name.lower().endswith('.pdf'):
            file_path = os.path.join(base_path, file_name)
            print(f"\nExtracting from: {file_name}")
            file_names.append(file_name)
            # print("\n")
            resume_text = extract_text_from_pdf(file_path)
            # print(resume_text[:100])
            # print("\n")
            email = extract_email(resume_text)
            phone = extract_phone(resume_text)
            name,linenumber = extract_name(email,resume_text)
            dict1=extract_district(resume_text)
            district=approx_place_identification(linenumber,dict1)
            print("Email:", email)
            print("Phone:", phone)
            print("Name:", name," ",linenumber)
            print("---",dict1,"---")
            print("place :",district)
            print("\n",'-'*10,"\n")
            list_of_details.append(name)
            list_of_details.append(phone)
            list_of_details.append(email)
            list_of_details.append(district)
            list_of_listdetails.append(list_of_details)
    final_details_dict={}
    if len(file_names)!=len(list_of_listdetails):
        print("!!!!!!!!! ERROR !!!!!!!!!!!!")
    for i,j in enumerate(file_names):
        final_details_dict[j]=list_of_listdetails[i]
    return final_details_dict


            