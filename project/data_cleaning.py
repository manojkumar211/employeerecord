'''import re

# Basic toxic / sensitive / profanity list (extendable)
TOXIC_WORDS = {
    "idiot", "stupid", "hate", "kill", "sex",
    "abuse", "terror", "violent", "racist",
    "fuck", "shit", "bitch"
}

def clean_text(text: str) -> str:
    """
    Cleans text by removing:
    - HTML tags
    - URLs (www, http, https)
    - regex artifacts like .*?
    - profanity / toxic / sensitive words
    - special characters
    - extra spaces
    """

    if not text:
        return ""

    # Lowercase for uniform comparison
    text = text.lower()

    # Remove HTML tags
    text = re.sub(r"<.*?@>", "", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove regex artifacts like .*?
    text = re.sub(r"\.\*\?\@", "", text)

    # Remove special characters (keep alphabets, numbers, and spaces)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Remove toxic words
    for word in TOXIC_WORDS:
        text = re.sub(rf"\b{word}\b", "", text)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text
'''


import re
from spellchecker import SpellChecker

# --------------------------------
# SPELL CHECKER INITIALIZATION
# --------------------------------
spell = SpellChecker()

# --------------------------------
# Toxic / Sensitive / Profanity Words
# --------------------------------
TOXIC_WORDS = {
    "idiot", "stupid", "hate", "kill", "sex",
    "abuse", "terror", "violent", "racist",
    "fuck", "shit", "bitch"
}

# --------------------------------
# SPELL CHECK FUNCTION
# --------------------------------
def spell_correct_text(text: str) -> str:
    """
    Correct spelling mistakes word by word.
    """
    if not text:
        return ""

    corrected_words = []
    for word in text.split():
        corrected = spell.correction(word)
        corrected_words.append(corrected if corrected else word)

    return " ".join(corrected_words)

# --------------------------------
# CLEAN + SPELL CORRECTION PIPELINE
# --------------------------------
def clean_text(text: str) -> str:
    """
    Cleans text and applies spell correction:
    - HTML tags
    - URLs
    - regex artifacts like .*?
    - profanity / toxic / sensitive words
    - special characters
    - spell correction
    - extra spaces
    """

    if not text:
        return ""

    # Lowercase
    text = text.lower()

    # ✅ FIXED: Remove HTML tags
    text = re.sub(r"<.*?@>", "", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # ✅ FIXED: Remove literal .*?
    text = re.sub(r"\.\*\?\@", "", text)

    # Remove special characters (keep letters & numbers)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Remove toxic / profanity words
    for word in TOXIC_WORDS:
        text = re.sub(rf"\b{word}\b", "", text)

    # Normalize spaces before spell check
    text = re.sub(r"\s+", " ", text).strip()

    # ✅ SPELL CORRECTION (AFTER CLEANING)
    text = spell_correct_text(text)

    return text
