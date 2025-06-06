Developed by Suchanda Bhattacharyya, Angelina Jordine, Marie Mehlfeldt on 5./6.06.2025 at CCLS Datathon (Aachen, organized by HDS-LEE)

Goal:
Create an online tool to extract data from doctor’s note (as pdf, English language), calculate the Framingham Heart Failure Risk Score from extracted data and/or manual inputs, give recommendations on preventative actions based on risk score and patient information, sends email to specifiable email address if critical values of vital parameters are reached
If the patient is sufficiently ill, this triggers an email to the doctor.

Methods:
Extracting data from pdf: RAG with structured output using agno
Giving recommendations: multiagentic system with RAG (agentic retrieval, duckduckgo agent)

How to use:
Create conda environment
Use pip install to install required libraries
Adjust sender email address, receiver email address, password for sending email
Run interface.py
Upload pdf and click on “extract from pdf”-button
Adjust patient data manually
Click on “give recommendations”-button

Limitations:
Agent to choose when email should be sent must be implemented


![Screenshot 2025-06-06 at 11 31 32](https://github.com/user-attachments/assets/4c55b97c-7873-4abd-bc5e-e2f2ab7c1aa6)
![Screenshot 2025-06-06 at 11 32 04](https://github.com/user-attachments/assets/8dfe4370-4cb3-49ba-b895-b7e75b60fa29)
![Screenshot 2025-06-06 at 11 36 21](https://github.com/user-attachments/assets/7180eb76-cc73-4d34-9be2-ff194672fbe3)
