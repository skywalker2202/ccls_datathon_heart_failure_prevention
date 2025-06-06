AzureEndpoint = "https://workshopccls.openai.azure.com/"
AzureOpenAIKey = "2xoDaxJZ8Z6oBzXl9UhxryKoHiAY9uetTdCeUfxmbRt58GZmOCbvJQQJ99BEACfhMk5XJ3w3AAABACOGkc4n"
model_name = "gpt-4.1-nano"
deployment = "gpt-4.1-nano"
from smolagents import AzureOpenAIServerModel
from smolagents import CodeAgent, DuckDuckGoSearchTool
api_version = "2025-04-01-preview"
import datetime
import smtplib, ssl
import random
import ast
import string
import random, string

# --- Email settings (replace with your own) ---


def generate_random_string(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Define patient abnormalities and category
patient_abnormalities = [
    "patient has a high bp of 200",
    "patient has a prior myocardial infarction", 
    "patient has diabetes mellitus type 2",
    "patient has elevated LDL cholesterol 180 mg/dL",
    "patient is a current smoker 15 pack-years"
]
 
# # Set patient risk category: "low", "mid", or "high"

# print(f"Patient Category: {patient_category}")
# print(f"Number of abnormalities: {len(patient_abnormalities)}")


Azure_smol = AzureOpenAIServerModel(
    api_version=api_version,
    azure_endpoint=AzureEndpoint,
    api_key=AzureOpenAIKey,
    model_id=deployment,temperature=0)
search_tool = DuckDuckGoSearchTool()



heart_prevention_agent_low = CodeAgent(
    name="heart_prevention_researcher_low",
    tools=[search_tool],
    model=Azure_smol,
    description="""You are a medical research assistant specialized in heart attack prevention. 
    Your purpose is to search for and summarize reliable information about simple, 
    evidence-based heart attack prevention strategies. Focus on lifestyle changes, 
    dietary recommendations, exercise guidelines, and early warning signs that 
    everyday people can understand and implement."""
)

heart_prevention_agent_mid = CodeAgent(
    name="midlevel_cardiac_risk_specialist",
    tools=[search_tool],
    model=Azure_smol,
    description="""You are a specialized medical research assistant focused on managing 
    intermediate cardiovascular risk levels. Your purpose is to search for and summarize 
    evidence-based strategies specifically for patients with midlevel heart attack risk scores 
    (10-year risk of 10-20% or intermediate risk categories). Focus on targeted interventions, 
    risk stratification refinement, monitoring protocols, and aggressive prevention strategies 
    for this specific risk population."""
)

high_search_agent = CodeAgent(
    name="high_search_agent",
    tools=[search_tool],
    model=Azure_smol,
    description="""You are a specialized medical research agent focused on patient 
    education and safe cardiovascular risk management. Your purpose is to search for 
    evidence-based, patient-friendly recommendations while identifying contraindications 
    and safety considerations. Always prioritize patient safety and avoid contradictory 
    advice based on specific medical conditions."""
)

def handle_low_risk_patient_enhanced(heart_prevention_agent_low):
    """
    Enhanced low-risk patient handler with logging and structured output
    """
    

    main_response = heart_prevention_agent_low.run("""
    Search for current information about simple heart attack prevention strategies. 
    Please find and summarize in simple layman and comforting language that is easy to understand for patients with no medical background:
    1. Key lifestyle changes for heart attack prevention
    2. Simple dietary modifications
    3. Exercise recommendations
    4. Early warning signs to watch for
    5. Risk factors people should be aware of

    Focus on evidence-based, actionable advice that ordinary people can follow.
    """)
    
    # print("📋 PREVENTION STRATEGIES:")
    # print("-" * 40)
    # print(main_response)
    
    # Daily habits follow-up
    follow_up_response = heart_prevention_agent_low.run(
        "What are the most important daily habits someone can adopt to prevent heart attacks?"
    )
    try:
        habits_list = ast.literal_eval(follow_up_response)
        habits_html = "<ul style='line-height: 1.6;'>" + "".join([f"<li>{habit}</li>" for habit in habits_list]) + "</ul>"
    except Exception:
        habits_html = f"<p style='line-height: 1.6;'>{follow_up_response}</p>"

   
    
    
    return_str = f"""
       📋 PREVENTION STRATEGIES:
       <p>{main_response}</p>
        
        📋 Daily habits:
       {habits_html}
        """
    return return_str    


def handle_midlevel_risk_patient_complete(heart_prevention_agent_mid, patient_abnormalities= patient_abnormalities):
    """
    Complete midlevel risk patient handler with combined responses for Gradio output
    """
    
    # Main midlevel risk management query
    response = heart_prevention_agent_mid.run("""
    Search for current clinical guidelines and research about managing midlevel/intermediate 
    heart attack risk scores. Please find and summarize Please find and summarize in simple
    layman and comforting language that is easy to understand for patients with no medical background
    1. Specific interventions for 10-20% 10-year cardiovascular risk patients
    4. Intensive lifestyle modification protocols
    5. Monitoring frequency and follow-up strategies
    6. When to escalate to cardiology referral

    Focus on evidence-based approaches specifically for intermediate risk patients, in a simple comforting language like a nice old doctor
    not general prevention or high-risk management.
    """)
    
    # Follow-up for daily monitoring strategies
    follow_up = heart_prevention_agent_mid.run("""
    What are the most effective daily monitoring and management strategies for someone 
    with a midlevel heart attack risk score? Include specific targets for blood pressure, 
    cholesterol, and lifestyle metrics that can move them from intermediate to low risk.
    """)
    
    # Risk score improvement strategies
    risk_improvement = heart_prevention_agent_mid.run("""
    What interventions have the strongest evidence for reducing cardiovascular risk scores 
    from intermediate (10-20%) to low risk (<10%) categories? Include timeframes and 
    measurable outcomes.
    """)
    patient_abnormalities_result = ""
    for i, abnormality in enumerate(patient_abnormalities, 1):
        search_result = heart_prevention_agent_mid.run(f"""
        Search for current medical information about: "{abnormality}"
        Please find and summarize in a simple comforting language like a nice old doctor giving actionble evidence based steps in 3 lines.
        Address the patient directly

        1. Clinical significance and severity assessment
        4. Evidence-based treatment recommendations
        5. Monitoring requirements and follow-up protocols
        
        Focus on recent clinical guidelines and evidence-based medicine.
        """)
        patient_abnormalities_result += f"{search_result} \n "


    
    return_str = f"""

    <div style="background-color: #fff3e0; padding: 20px; border-radius: 10px; border-left: 5px solid #ff9800;">
        <h2 style="color: #e65100; margin-top: 0;">🔶 MIDLEVEL CARDIAC RISK MANAGEMENT CONSULTATION</h2>
        
        <div style="background-color: #fafafa; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <h3 style="color: #e65100;">📋 CLINICAL GUIDELINES & INTERVENTIONS</h3>
            <p style="line-height: 1.6;">{response}</p>
        </div>
        
        <div style="background-color: #fafafa; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <h3 style="color: #e65100;">📊 DAILY MONITORING & MANAGEMENT STRATEGIES</h3>
            <p style="line-height: 1.6;">{follow_up}</p>
        </div>
        
        <div style="background-color: #fafafa; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <h3 style="color: #e65100;">📈 RISK SCORE REDUCTION STRATEGIES</h3>
            <p style="line-height: 1.6;">{risk_improvement}</p>
        </div>
        
        <div style="background-color: #fafafa; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <h3 style="color: #e65100;">📈 ABNORMALITIES</h3>
            <p style="line-height: 1.6;">{patient_abnormalities_result}</p>
        </div>
    </div>
    """
    
    return return_str

def handle_high_risk_patient(high_search_agent, patient_abnormalities, high_alert ):
        patient_abnormalities_result = ""
        for i, abnormality in enumerate(patient_abnormalities, 1):
            search_result = heart_prevention_agent_mid.run(f"""
            Search for current medical information about: "{abnormality}"
            
            Please find and summarize in a simple comforting language like a nice old doctor giving actionble evidence based steps in 3 lines.
            Address the patient directly
            4. Evidence-based treatment recommendations
            5. Monitoring requirements and follow-up protocols
            
            Focus on recent clinical guidelines and evidence-based medicine.
            """)
            patient_abnormalities_result += f" {search_result} \n "

        
        return_str = f"""
                🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴
                 CRITICAL: HIGH-RISK PATIENT DETECTED
                 Hospital alerted
                📈 Key areas to look for 
                <p style="line-height: 1.6;">{patient_abnormalities_result}</p>
                """
        return return_str
    



    
    
def select_patient_agent_complete(patient_category, heart_prevention_agent_low, 
                                 heart_prevention_agent_mid, high_search_agent):
    """
    Complete patient agent selection with all risk categories
    """
    
    agent = None
    response_data = None
    
    if patient_category == "low":
        agent = heart_prevention_agent_low
        response_data = handle_low_risk_patient_enhanced(heart_prevention_agent_low)
        
    elif patient_category == "mid":
        agent = heart_prevention_agent_mid
        response_data = handle_midlevel_risk_patient_complete(heart_prevention_agent_mid, patient_abnormalities = patient_abnormalities)
        
    elif patient_category == "high":
        agent = high_search_agent
        response_data = handle_high_risk_patient(high_search_agent, patient_abnormalities = patient_abnormalities, high_alert=high_alert)

        
    else:
        raise ValueError(f"Invalid patient category: {patient_category}. Must be 'low', 'mid', or 'high'")
    
    return agent, response_data

def save_patient_consultation( consultation_data):
    """Save consultation data for patient records"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/Users/suchanda/Desktop/CCLS-Datathon-2025/proj/consultation_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            if "combined_summary" in consultation_data:
                f.write(consultation_data["combined_summary"])
            else:
                f.write(str(consultation_data))
        
        print(f"✅ Consultation saved to: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error saving consultation: {e}")
        return None


def run (patient_category, patient_abnormalities, high_alert):
    try:
        if patient_category == "low":
            print("Processing s-RISK patient...")
            consultation_results = handle_low_risk_patient_enhanced(
                heart_prevention_agent_low
            )
            return consultation_results
            
        elif patient_category == "mid":
            print("Processing MID-LEVEL RISK patient...")
            consultation_results = handle_midlevel_risk_patient_complete(heart_prevention_agent_mid, patient_abnormalities)
            return consultation_results
        elif patient_category == "high":
            SENDER_EMAIL = "angelinajordine@gmail.com"
            SENDER_PASSWORD = "ytsu rlgi xjma osqr"
            RECEIVER_EMAIL = "bhattacharyya.s2202@gmail.com"


            print("Processing HIGH-RISK patient...")
            emergency_results = handle_high_risk_patient(high_search_agent= high_search_agent,patient_abnormalities = patient_abnormalities, high_alert= high_alert)
            subject = f"PATIENT DYING: ATTEND IMMEDIETLY"
            message_body = f"PATIENT DYING:\n\n PATIENT DYING: ATTEND IMMEDIETLY"
            full_message = f"PATIENT DYING: {subject}\n\n{message_body}"

            context = ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(SENDER_EMAIL, SENDER_PASSWORD)
                    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, full_message)
                print("✅ Email sent successfully!")
            except Exception as e:
                print(f"❌ Failed to send email: {e}")
        
            
        print(f"\n✅ Patient consultation completed for category: {patient_category}")
        return emergency_results
            
    except Exception as e:
        print(f"❌ Error during consultation: {e}")
        print("Please check your configuration and try again.")



