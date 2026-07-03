import streamlit as st
import json
import enchant
from datetime import datetime

# Configure page settings for better UI
st.set_page_config(page_title="Symptom Tracker", layout="centered")

# Initialize English dictionary from enchant library for word validation
d = enchant.Dict("en_US")

# Set of all valid body parts that user can enter - prevents random input
allowed_body_parts = {
    "left", "right", "upper", "lower", "skin", "eye", "eyes", "ear", "ears", "nose", "tongue",
    "brain", "cerebrum", "cerebellum", "brainstem", "spinal cord", "heart",
    "artery", "arteries", "vein", "veins", "capillary", "capillaries", "pharynx", "throat",
    "larynx", "voice box", "trachea", "windpipe", "bronch", "bronchi", "lung", "lungs",
    "diaphragm", "mouth", "tooth", "teeth", "salivary gland", "salivary glands",
    "parotid", "submandibular", "sublingual", "esophagus", "stomach",
    "small intestine", "duodenum", "jejunum", "ileum", "large intestine", "cecum",
    "colon", "rectum", "appendix", "anus", "liver", "gallbladder", "pancreas",
    "mesentery", "abdomen", "kidney", "kidneys", "ureter", "ureters",
    "urinary bladder", "urethra", "pituitary gland", "pineal gland",
    "thyroid gland", "parathyroid gland", "parathyroid glands", "adrenal gland",
    "adrenal glands", "thymus", "spleen", "lymph node", "lymph nodes", "tonsil",
    "tonsils", "palatine", "pharyngeal", "adenoid", "adenoids", "lingual",
    "bone marrow", "bone", "bones", "skeletal muscle", "skeletal muscles",
    "tendon", "tendons", "ligament", "ligaments", "tendons and ligaments", "joint",
    "joints", "articulation", "articulations", "testis", "testes", "epididymis",
    "vas deferens", "seminal vesicle", "seminal vesicles", "prostate gland",
    "bulbourethral gland", "bulbourethral glands", "cowper's gland", "cowper's glands",
    "penis", "ovary", "ovaries", "fallopian tube", "fallopian tubes", "uterus",
    "vagina", "vulva", "clitoris", "labia majora", "labia minora", "placenta",
    "mammary gland", "mammary glands", "breast", "breasts", "interstitium"
}


def is_valid_body_part(answer):
    normalized = answer.strip().lower()
    if not normalized:
        return False
    
    # Check if exact match exists in allowed body parts
    if normalized in allowed_body_parts:
        return True
    
    # Check if input starts with direction prefix (left/right/upper/lower)
    words = normalized.split()
    if len(words) >= 2 and words[0] in {"left", "right", "upper", "lower"}:
        return " ".join(words[1:]) in allowed_body_parts
    
    return False

def validate_symptoms(value):
    if not value.strip():
        return False
    words = value.split()
    # Check if all words contain only letters
    if any(not word.isalpha() for word in words):
        return False
    # Check if all words exist in English dictionary
    return all(d.check(word.lower()) for word in words)

def validate_triggers(value):
    if not value.strip():
        return False
    words = value.split()
    if any(not word.isalpha() for word in words):
        return False
    return all(d.check(word.lower()) for word in words)

def normalize_time(years, months, weeks, days, hours):
    while hours >= 24:
        hours -= 24
        days += 1
    
    while days >= 7:
        days -= 7
        weeks += 1
    
    while weeks >= 4:
        weeks -= 4
        months += 1
    
    while months >= 12:
        months -= 12
        years += 1
    
    return years, months, weeks, days, hours


st.title("🏥 Symptom Tracker")
st.write("Please describe your symptoms below. Answer the following questions:")

# Visual separator for clean layout
st.markdown("---")

st.subheader("1. Symptoms")
symptoms = st.text_input(
    "What symptoms do you have?",
    placeholder="e.g., fever, headache, cough"
)

if symptoms and not validate_symptoms(symptoms):
    st.error("⚠️ Please write a real symptom (letters only, real English words)")

st.subheader("2. Body Part")
body_part = st.text_input(
    "Which body part is affected?",
    placeholder="e.g., head, left eye, upper abdomen"
)

if body_part and not is_valid_body_part(body_part):
    st.error("⚠️ Please enter a valid body part")

st.subheader("3. Severity")
severity = st.slider(
    "How severe are they? (0 = No pain, 10 = Worst pain)",
    min_value=0,
    max_value=10,
    value=5,
    step=1
)

st.subheader("4. Triggers")
triggers = st.text_input(
    "Anything that makes them better or worse?",
    placeholder="e.g., cold, rest, exercise"
)

if triggers and not validate_triggers(triggers):
    st.error("⚠️ Please write a real trigger (letters only, real English words)")

st.subheader("5. When Did It Start?")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    years = st.number_input("Years", min_value=0, max_value=100, value=0)

with col2:
    months = st.number_input("Months", min_value=0, max_value=12, value=0)

with col3:
    weeks = st.number_input("Weeks", min_value=0, max_value=52, value=0)

with col4:
    days = st.number_input("Days", min_value=0, max_value=30, value=0)

with col5:
    hours = st.number_input("Hours", min_value=0, max_value=24, value=0)

# Visual separator before submission section
st.markdown("---")

if st.button("📤 Submit", use_container_width=True):
    errors = []
    
    if not symptoms:
        errors.append("Symptoms are required")
    elif not validate_symptoms(symptoms):
        errors.append("Please enter a real symptom")
    
    if not body_part:
        errors.append("Body part is required")
    elif not is_valid_body_part(body_part):
        errors.append("Please enter a valid body part")
    
    if not triggers:
        errors.append("Triggers are required")
    elif not validate_triggers(triggers):
        errors.append("Please enter a real trigger")
    
    if errors:
        for error in errors:
            st.error(f"❌ {error}")
    else:
        
        norm_years, norm_months, norm_weeks, norm_days, norm_hours = normalize_time(
            int(years), int(months), int(weeks), int(days), int(hours)
        )
        
        data = {
            "symptoms": symptoms,
            "body_part": body_part,
            "severity": int(severity),
            "triggers": triggers,
            "started": {
                "years": norm_years,
                "months": norm_months,
                "weeks": norm_weeks,
                "days": norm_days,
                "hours": norm_hours
            },
            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save collected data to JSON file
        with open("symptom_data.json", "w") as file:
            json.dump(data, file, indent=4)
        
        st.success("✅ Data saved successfully!")
        
        st.subheader("📋 Summary")
        st.json(data)
        
        st.download_button(
            label="📥 Download as JSON",
            data=json.dumps(data, indent=4),
            file_name="symptom_data.json",
            mime="application/json"
        )
