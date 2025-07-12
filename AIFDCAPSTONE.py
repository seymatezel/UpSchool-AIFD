import re

def analyze_cv(cv_text):
    strengths = []
    weaknesses = []

    if "takım çalışması" in cv_text.lower():
        strengths.append("Takım çalışması")
    if "problem çözme" in cv_text.lower():
        strengths.append("Problem çözme")

    if len(cv_text) < 300:
        weaknesses.append("CV çok kısa olabilir, detay eksikliği")

    return strengths, weaknesses

if __name__ == "__main__":
    cv = input("CV metnini yapıştırın:\n")
    strengths, weaknesses = analyze_cv(cv)

    print("\nGüçlü Yönler:")
    for s in strengths:
        print("- " + s)
    print("\nZayıf Yönler:")
    for w in weaknesses:
        print("- " + w)