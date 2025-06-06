import numpy as np
import gradio as gr
from agent_selector import run
from extract_pdf import extract_data_from_pdf

def wrap_inputs_to_dict(age, sbp, bp_med, lvh, gender, bmi, heart_rate, pmi, vhd):
    return calculate_FHFRS({
        "Age": age,
        "SBP": sbp,
        "BP_med": bp_med,
        "LVH (ECG)": lvh,
        "Gender": gender,
        "BMI": bmi,
        "Heart_Rate": heart_rate,
        "PMI": pmi,
        "VHD": vhd
    })

def calculate_FHFRS(dictionary):
    score = 0
    alert_string = []
    high_alert_list = []

    # age
    if dictionary['Age'] >= 55:
        score = score + 5
    if dictionary['Age'] >= 65:
        score = score + 5
    if dictionary['Age'] >= 75:
        score = score + 5
    if dictionary['Age'] >= 85:
        score = score + 5
    if dictionary['Age'] >= 95:
        score = score + 5

    # systolic blood pressure
    if dictionary['SBP'] >= 160:
        score = score + 1
    if dictionary['SBP'] > 140:
        alert_string.append(f"Systolic blood pressure is high with a value of {dictionary['SBP']} mmHg. ")
    if dictionary['SBP'] >= 200:
        high_alert_list.append('Systolic blood pressure is critically high with a value of ' + str(dictionary['SBP']) + ' mmHg.')

    # use of blood pressure medicine
    if dictionary['BP_med'] == 1 or dictionary['BP_med'] == True:
        score = score + 2
        alert_string.append('Patient is on blood pressure medication. ')

    # patient shows signs of left ventricular hypertrophy in the ECG
    if dictionary['LVH (ECG)'] == 1 or dictionary['LVH (ECG)'] == True:
        if dictionary['Gender'] == 'female':
            score = score + 5
        else:
            score = score + 4
        alert_string.append('Patient shows signs of left ventricular hypertrophy in the ECG. ')

    # BMI
    if dictionary['BMI'] >= 30:
        score = score + 2
    if dictionary['BMI'] >= 25:
        alert_string.append(f'Patient has a high BMI of {dictionary["BMI"]}. ')
    elif dictionary['BMI'] <= 18.5:
        alert_string.append('Patient has a low BMI of ' + str(dictionary['BMI']) + '.')

    # heart rate
    if dictionary['Heart_Rate'] >= 90:
        score = score + 3
    if dictionary['Heart_Rate'] >= 100:
        alert_string.append(f'Heart Rate is high with a value of {dictionary["Heart_Rate"]} bpm. ')
    elif dictionary['Heart_Rate'] <= 60:
        alert_string.append(f'Heart Rate is low with a value of {dictionary["Heart_Rate"]} bpm. ')
    if dictionary['Heart_Rate'] >= 180:
        high_alert_list.append('Heart rate is critically high with a value of ' + str(dictionary['Heart_Rate']) + ' bpm.')

    # prior myocardial infarction
    if dictionary['PMI'] == 1 or dictionary['PMI'] == True:
        score = score + 7
        alert_string.append('Patient has a prior myocardial infarction. ')
    
    # valvular heart disease
    if dictionary['VHD'] == 1 or dictionary['VHD'] == True:
        score = score + 3
        alert_string.append('Patient has valvular heart disease. ')

    risk_strat, risk_string = stratify_risk(dictionary, score)

    return score, risk_strat, risk_string, alert_string, high_alert_list

def stratify_risk(dict, score):
    if dict['Gender'] == 'female':
        if score <= 5:
            risk = (0, 1)
            risk_strat = 'low'
        elif score >= 6 and score <= 10:
            risk = (1, 3)
            risk_strat = 'mid'
        elif score >= 11 and score <= 15:
            risk = (3, 8)
            risk_strat = 'mid'
        elif score >= 16 and score <= 20:
            risk = (8, 15)
            risk_strat = 'mid'
        else:
            risk = (15, np.inf)
            risk_strat = 'high'
    else:
        if score <= 5:
            risk = (0, 1)
            risk_strat = 'low'
        elif score >= 6 and score <= 10:
            risk = (2, 5)
            risk_strat = 'mid'
        elif score >= 11 and score <= 15:
            risk = (5, 10)
            risk_strat = 'mid'
        elif score >= 16 and score <= 20:
            risk = (10, 20)
            risk_strat = 'mid'
        else:
            risk = (20, np.inf)
            risk_strat = 'high'

    if np.inf in risk:
        risk_string = f'>{risk[0]}%'
    elif 0 in risk:
        risk_string = f'<{risk[1]}%'
    else:
        risk_string = f'{risk[0]}-{risk[1]}%'

    return risk_strat, risk_string

def extract_patient_data_from_pdf(file):
    return {
        "age": 77,
        "SBP": 172,
        "BP med": True,
        "LVH (ECG)": True,
        "gender": "female",
        "BMI": 32.5,
        "heart rate": 120,
        "PMI": True,
        "VHD": True
    }
from pydantic import BaseModel, Field
from agno.embedder.azure_openai import AzureOpenAIEmbedder
from agno.models.azure import AzureOpenAI
from agno.agent import Agent
import os
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from io import BytesIO

class Relevent_Data(BaseModel):
    age: float = Field(description="age of patient")
    SBP: float = Field(description="systolic blood pressure")
    BP_med: int = Field(description="use of blood pressure medication")
    LVH_ECG: int = Field(description="left ventricular hypertrophy in the ECG")
    Gender: str = Field (description="gender (female of male)")
    BMI: float = Field (description="BMI (body mass index in kg/m^2)")
    Heart_Rate: float = Field (description="heart rate in beats per minute")
    PMI:int = Field(description="previous myocardial infarction")
    VHD: int = Field(description="ventricular heart disease")

class Relevant_Data_List(BaseModel):
    relevant_data: list[Relevent_Data] = Field(description="List of relevant data")

import tempfile
import os


def extract_patient_data_from_pdf(file):
    model_name = "gpt-4.1-mini"
    api_version = "2025-04-01-preview"
    endpoint = "https://workshopccls.openai.azure.com/"
    api_key = "2xoDaxJZ8Z6oBzXl9UhxryKoHiAY9uetTdCeUfxmbRt58GZmOCbvJQQJ99BEACfhMk5XJ3w3AAABACOGkc4n"

    os.environ["AZURE_OPENAI_API_KEY"] = api_key
    os.environ["AZURE_OPENAI_ENDPOINT"] = endpoint
    os.environ["OPENAI_API_VERSION"] = api_version

    vector_db = ChromaDb(
        collection="ccls",
        embedder=AzureOpenAIEmbedder(id='text-embedding-3-small')
    )

    # 📂 Temporäre Datei anlegen und Inhalt schreiben
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file)
        tmp_path = tmp.name  # Merke Pfad der Datei

    # 🧠 Knowledge Base mit 'path' erzeugen
    knowledge_base = PDFKnowledgeBase(
        path=tmp_path,
        vector_db=vector_db,
        reader=PDFReader(chunk=True),
    )

    agent = Agent(
        model=AzureOpenAI(id=model_name),
        knowledge=knowledge_base,
        instructions=[
            "Cite the exact phrases and section titles from the sources in your response.",
            "Use enumerations to organize your response.",
            "Do not write any other text than the response.",
        ],
        response_model=Relevant_Data_List,
        search_knowledge=True,
    )

    agent.knowledge.load()
    res = agent.run("List the relevant data from the doctor's note.")
    data_dict = res.content.relevant_data[0].model_dump()

    # 🔒 Aufräumen (optional)
    os.remove(tmp_path)

    return data_dict



def calculate_and_print_results(age, sbp, bp_med, lvh, gender, bmi, heart_rate, pmi, vhd):
    """Calculate FHFRS and print combined results to terminal"""
    if age is None or sbp is None or gender is None or bmi is None or heart_rate is None:
        print("Please fill in all required fields.")
        return "Calculation incomplete - missing required fields"
    
    score, strat_output, risk_output, alert_output, high_alert_output = wrap_inputs_to_dict(
        age, sbp, bp_med, lvh, gender, bmi, heart_rate, pmi, vhd
    )


    agent_output = run(strat_output, alert_output, high_alert_output)
    
    status = f"✅ Calculation complete \n::  Risk Category: {strat_output}\n Risk Percentage: {risk_output}"
    
    return agent_output, status

    
def interface():
    with gr.Blocks() as demo:
        gr.Markdown("## FHFRS Risiko-Score mit PDF-Vorbefüllung")

        with gr.Row():
            pdf_input = gr.File(label="PDF hochladen", type= "binary")
            load_button = gr.Button("Daten aus PDF extrahieren")

        with gr.Row():
            age = gr.Number(label="Alter")
            sbp = gr.Number(label="Systolischer Blutdruck (SBP)")
            bp_med = gr.Checkbox(label="Blutdruckmedikation (BP med)")
            lvh = gr.Checkbox(label="Linksventrikuläre Hypertrophie (LVH, ECG)")
            gender = gr.Radio(["Male", "Female"], label="Geschlecht")
            bmi = gr.Number(label="BMI")
            heart_rate = gr.Number(label="Herzfrequenz")
            pmi = gr.Checkbox(label="Frühere Myokardinfarkte (PMI)")
            vhd = gr.Checkbox(label="Klappenerkrankung (VHD)")


        # PDF-Upload fills the fields (still editable)
        def fill_fields_from_pdf(file):
            data = extract_patient_data_from_pdf(file)
            return (
                data["age"], data["SBP"], data["BP_med"], data["LVH_ECG"],
                data["Gender"], data["BMI"], data["Heart_Rate"], data["PMI"], data["VHD"]
            )


        load_button.click(
            fn=fill_fields_from_pdf,
            inputs=pdf_input,
            outputs=[age, sbp, bp_med, lvh, gender, bmi, heart_rate, pmi, vhd]
        )

        gr.Markdown("### Risiko-Auswertung")
        calc_button = gr.Button("Score berechnen")
        
        # Simple status output for user feedback
        status_output = gr.Textbox(label="Status", interactive=False)

        calc_button.click(
            fn=calculate_and_print_results,
            inputs=[age, sbp, bp_med, lvh, gender, bmi, heart_rate, pmi, vhd],

            outputs=status_output
        )

    demo.launch()

if __name__ == "__main__":
    interface()
