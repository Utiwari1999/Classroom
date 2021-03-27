# Plagiarism Checker

## Introduction
*Plagiarism, the act of taking the writings of another person and passing them off as one’s own.   The   fraudulence is   closely   related   to   forgery   and   piracy-practices   generally   in violation of copyright laws. as quoted by Encyclopedia Britannica.*

Our project idea focuses on developing a plagiarism checker on an online classroom using where an educator can detect the extent of plagiarism in the assignment submitted by the students, and also check whether two students have copied assignment from each other. We studied various research papers published in this field along with some exciting plagiarism detection algorithms and looked upto some previously existing applications in this domain. 

## Scope of Project
It includes various requirements like finding the right API which has lowest latency and gives us quick results. Tokenization , which parses, tokenizes and preprocess the documents. Our next requirement was to highlight copied sentences and its corresponding coped sentence in another document whenever we find a plagiarized sentence between two documents. Our final goal is to provide two options for the educator to choose whether to check plagiarism from the internet, which tells us what are the corresponding links and copied percentage beside the link using cosine similarity function, while the other option  checks plagiarism among assignments submitted by two students, and the similar sentence will be highlighted among them.


## Front End
HTML, CSS and Javascript.

## Back End
Django

## Setup/Installation
1. Clone the repository using https/ssh
```sh
git clone https://github.com/Utiwari1999/Classroom.git
```

2. Create a virtual environment
```sh
pip install virtualenv
virtualenv venv
```

- Activate virtual environment (macOS or Linux)
```sh
source venv/Scripts/activate
```

- Activate virtual environment (Windows)
```sh
venv\Scripts\activate 
```

3. Installing requirements
```sh
pip install -r requirement.txt
```

4. Set Database (Make Sure you are in directory same as manage.py)
```sh
python manage.py makemigrations
python manage.py migrate
```

5. Create SuperUser 
```sh
python manage.py createsuperuser
```
After all these steps , you can start using and developing this project. 

#### That's it! Happy Coding!
