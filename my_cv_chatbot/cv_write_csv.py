import csv


education = [
    "I earned an MA in Applied Linguistics and TESOL with Distinction from the University of Leicester in the UK, completing the program between 2016 and 2019.",
    "In 2018, I obtained a PGCE in Secondary Education with a focus on Modern Foreign Languages, achieving Qualified Teacher Status and NQT, from the University of Brighton in the UK.",
    "I completed the Cambridge DELTA at ILA in Vietnam between 2015 and 2016, earning two Merits and a Distinction.",
    "I received the Trinity TYLEC certification through the British Council in Vietnam in 2015.",
    "In 2011, I achieved the Cambridge CELTA qualification at International House in Belfast, Northern Ireland.",
    "I graduated with a BA (Honours) in Humanities with a focus on Spanish, earning a 2:1, from The Open University in the UK, completing the degree between 2003 and 2012.",
    "I was awarded a Certificate in Spanish with Distinction from The Open University in the UK, having completed the coursework between 2007 and 2009."
    ]
qualifications = [
    "I completed the CS50p Programming with Python course through Harvard University in 2024.",
    "I am currently undertaking the Data Scientist: Natural Language Processing Specialist certification through Codecademy in 2024.",
    "In 2024, I earned a certification in Learn Git and GitHub from Codecademy, along with completing the Learn the Command Line course.",
    "I obtained the Certificate in Responsive Web Design from FreeCodeCamp in 2023.",
    "In 2022, I was awarded the Google Data Analytics Certificate from Google."
    ]
work = [
    "As the Founder and Director of BuddyApp Ltd. (2024 - present), I have been responsible for developing both the frontend and backend of the application, as well as creating and implementing APIs. I troubleshoot issues and bugs, write and implement custom code using JavaScript and React Native, and oversee the development and execution of the business plan. My role also involves conducting market research, leading marketing campaigns, and managing the company’s social media presence.",
    "In my role as a Content and Item Writer (Oxford International Education Group; Trinity College London; British Council, 2022 – present), I work on extended content projects covering speaking, listening, reading, and writing, specifically focused on online assessment content. My responsibilities include content maintenance, quality assurance, and collaborating remotely with international teams to ensure the highest standards are met.",
    "As Head of English at Shackleton International School (Valencia, Spain, 2022 – 2024), I was responsible for designing and developing curriculum and assessment materials, including schemes of work, lesson scripts, and vocabulary lists. I liaised with heads of department to align educational aims and objectives and played a key role in improving literacy across the school by organising subject-related events, activities, and outings.",
    "At the British School Alzira (Valencia, Spain, 2019 – 2022), I taught English to students in KS3, KS4 (GCSE English Language and Literature), and KS5 (AS and A Level English). I also contributed to curriculum and assessment design and development, crafting schemes of work, lesson scripts, and vocabulary lists to enhance the educational experience.",
    "As a Modern Foreign Languages teacher at The Angmering School (Spanish and French, UK, 2018 – 2019), I wrote and delivered lessons in Spanish and French, developing curriculum and assessment materials for KS3 and KS4. My role focused on creating engaging schemes of work that facilitated language acquisition and cultural understanding.",
    "During my time as a Teacher Trainer with The Distance DELTA (UK, 2016 – 2017), I led formal observations and provided detailed feedback and instruction to trainee teachers. I also coordinated external observations, ensuring that all training met the rigorous standards required for certification.",
    "As a Teacher of English and Line Manager at the British Council in Vietnam (2013 – 2017), I served as a level leader and mentor, providing guidance and support to colleagues. I was also a tutor and trainer on the Trinity TYLEC, delivering induction and INSETTs, and creating online pedagogy courses for teachers. My teaching responsibilities included delivering lessons in general English, EAP, and IELTS to both young learners and adults."
    ]

with open("project.csv", "w", newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["education", "qualifications", "work"])
    writer.writeheader()

    # Determine the maximum length of the lists
    max_length = max(len(education), len(qualifications), len(work))

    for i in range(max_length):
        row = {
            "education": education[i] if i < len(education) else "",
            "qualifications": qualifications[i] if i < len(qualifications) else "",
            "work": work[i] if i < len(work) else ""
        }
        writer.writerow(row)