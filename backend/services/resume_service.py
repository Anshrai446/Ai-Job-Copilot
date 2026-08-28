import re


STOPWORDS = {
    "the", "and", "for", "with", "a", "an", "to", "of", "in",
    "on", "at", "by", "is", "are", "looking", "developer",
    "experience", "knowledge", "skills", "work",
    "backend", "frontend", "engineer"
}


SKILLS = {
    "java", "python", "sql", "javascript", "react", "node", "spring",
    "boot", "flask", "django", "mongodb", "mysql", "aws", "docker",
    "kubernetes", "html", "css", "rest", "api"
}


WEIGHTS = {
    "java": 3,
    "spring boot": 4,
    "sql": 3,
    "mysql": 3,
    "aws": 2,
    "docker": 2,
    "kubernetes": 2,
    "rest api": 2,
    "html": 1,
    "css": 1,
    "javascript": 1
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.split()


def extract_keywords(words):
    return {
        word for word in words
        if len(word) > 2 and word not in STOPWORDS
    }


def extract_skills_section(text):
    lines = text.lower().split("\n")

    skills_section = []
    capture = False

    for line in lines:

        if any(keyword in line for keyword in ["skill", "technology", "tools"]):
            capture = True
            continue

        if capture and ("education" in line or "experience" in line):
            break

        if capture:
            skills_section.append(line)

    return " ".join(skills_section)


def extract_phrases(text):
    text = text.lower()
    phrases = set()

    if "rest api" in text or "rest apis" in text:
        phrases.add("rest api")

    if "spring boot" in text:
        phrases.add("spring boot")

    return phrases


def normalize_keywords(keywords):
    normalized = set(keywords)

    if "rest api" in normalized:
        normalized.discard("rest")
        normalized.discard("apis")

    if "spring boot" in normalized:
        normalized.discard("spring")
        normalized.discard("boot")

    return normalized


def calculate_weighted_score(matched, jd_final):
    matched_score = sum(
        WEIGHTS.get(skill, 1)
        for skill in matched
    )

    total_score = sum(
        WEIGHTS.get(skill, 1)
        for skill in jd_final
    )

    return (matched_score / total_score) * 100 if total_score else 0


def analyze_resume(raw_resume, jd_text):

    skills_section = extract_skills_section(raw_resume)

    resume_text = (
        skills_section
        if skills_section.strip()
        else raw_resume
    )

    # Step 1: base words
    resume_words = set(clean_text(resume_text))
    jd_words = set(clean_text(jd_text))

    # Step 2: known skills
    resume_skills = resume_words.intersection(SKILLS)
    jd_skills = jd_words.intersection(SKILLS)

    # Step 3: dynamic keywords
    resume_keywords = extract_keywords(resume_words)
    jd_keywords = extract_keywords(jd_words)

    # Step 4: create final sets
    resume_final = resume_skills.union(resume_keywords)
    jd_final = jd_skills.union(jd_keywords)

    # Step 5: phrase detection
    resume_phrases = extract_phrases(resume_text)
    jd_phrases = extract_phrases(jd_text)

    resume_final = resume_final.union(resume_phrases)
    jd_final = jd_final.union(jd_phrases)

    # Step 6: normalization
    resume_final = normalize_keywords(resume_final)
    jd_final = normalize_keywords(jd_final)

    # Step 7: matching
    matched = resume_final.intersection(jd_final)
    missing = jd_final - resume_final

    # Step 8: weighted scoring
    match_score = calculate_weighted_score(
        matched,
        jd_final
    )

    return {
        "match_score": round(match_score, 2),
        "matched_keywords": sorted(list(matched)),
        "missing_keywords": sorted(list(missing))
    }