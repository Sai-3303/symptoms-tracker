import enchant
import json

print("Please describe your symptoms below")
print("You will be asked a few simple questions.\n")

questions = {
    "symptoms": "What symptoms do you have?\n ",
    "body_part": "Which body part is affected?\n ",
    "severity": "How severe are they? (0-10)\n ",
    "triggers": "Anything that makes them better or worse?\n "
}

answers = {}

# Initialize English dictionary from enchant library for word validation
d = enchant.Dict("en_US")

# Set of all valid body parts that user can enter
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


def ask_until_valid(prompt, validator, error_message, transform=None):
    while True:
        value = input(prompt).strip()
        if validator(value):
            # Apply optional transformation (e.g., convert to int)
            return transform(value) if transform else value
        print(error_message)


def validate_symptoms(value):
    words = value.split()
    if not words:
        return False
    # Check if all words contain only letters
    if any(not word.isalpha() for word in words):
        return False
    # Check if all words exist in English dictionary
    return all(d.check(word.lower()) for word in words)


def validate_triggers(value):
    words = value.split()
    if not words:
        return False
    if any(not word.isalpha() for word in words):
        return False
    return all(d.check(word.lower()) for word in words)


def validate_severity(value):
    return value.isdigit() and 0 <= int(value) <= 10


def validate_integer(value):
    if value.isdigit():
        return True
    if value.startswith("-") and value[1:].isdigit():
        return False
    return False


def get_valid_integer(prompt, label):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        if value.startswith("-") and value[1:].isdigit():
            print(f"Please enter a non-negative integer for {label}.")
        else:
            print(f"Please enter an integer for {label}.")

#Take excess years hours to days, days to weeks, weeks to months, months to years
def normalize_started(started):
    while started["hours"] >= 24:
        started["hours"] -= 24
        started["days"] += 1

    while started["days"] >= 7:
        started["days"] -= 7
        started["weeks"] += 1

    while started["weeks"] >= 4:
        started["weeks"] -= 4
        started["months"] += 1

    while started["months"] >= 12:
        started["months"] -= 12
        started["years"] += 1


answers["symptoms"] = ask_until_valid(
    questions["symptoms"],
    validate_symptoms,
    "Please write a real symptom."
)

answers["body_part"] = ask_until_valid(
    questions["body_part"],
    is_valid_body_part,
    "Please enter a valid body part."
)

answers["severity"] = ask_until_valid(
    questions["severity"],
    validate_severity,
    "Please enter a numerical value from 0 to 10.",
    transform=int
)

answers["triggers"] = ask_until_valid(
    questions["triggers"],
    validate_triggers,
    "Please enter, what triggers your symptoms."
)


print("\nWhen did it start?")
started = {}
started["years"] = get_valid_integer("Years: ", "years")
started["months"] = get_valid_integer("Months: ", "months")
started["weeks"] = get_valid_integer("Weeks: ", "weeks")
started["days"] = get_valid_integer("Days: ", "days")
started["hours"] = get_valid_integer("Hours: ", "hours")

normalize_started(started)
answers["started"] = started


print("\nSummary:")
for key, value in answers.items():
    if isinstance(value, dict):
        print(f"{key}:")
        for sub_key, sub_value in value.items():
            print(f"  {sub_key}: {sub_value}")
    else:
        print(f"{key}: {value}")

with open("symptom_data.json", "w") as file:
    json.dump(answers, file, indent=4)
    print("\nData saved to symptom_data.json")

