import subprocess
import os

def download_pastpaper(subject: str, code: str, D1: str, D2: str, year: str, p: str = "qp"):
    url = "https://pastpapers.co/cie/IGCSE/"

    # Determine exam series
    if D1 == "F" and D2 == "M":
        series = "March"
        s1 = "Mar"
        s2 = "m"
    elif D1 == "M" and D2 == "J":
        series = "May-June"
        s1 = "Mar"
        s2 = "s"
    elif D1 == "O" and D2 == "N":
        series = "Oct-Nov"
        s1 = "Nov"
        s2 = "w"
    else:
        print(f"Invalid series: {D1}{D2}")
        return

    subjects = {
        "0620": "Chemistry",
        "0610": "Biology",
        "0625": "Physics",
    }

    subname = subjects.get(subject)
    if not subname:
        print(f"Unknown subject: {subject}")
        return

    base_url = url + f"{subname}-{subject}"
    if int(year) <= 17:
        base_url += f"/20{year}/20{year}%20{s1}/"
    else:
        base_url += f"/20{year}-{series}/"

    filename = f"{subject}_{s2}{year}_{p}_{code}.pdf"
    full_path = f"C:/Users/Ant/Documents/pastpapers/{filename}"
    full_url = base_url + filename

    print(f"Downloading: {full_url}")
    result = subprocess.run(["curl", full_url, "--output", full_path], shell=True)

    if result.returncode == 0:
        print(f"Saved to: {full_path}")
    else:
        print(f"Failed to download: {full_url}")


# === Bulk Downloader ===
subjects = ["0620", "0625", "0610"]
codes = ["21", "22", "23"]
years = [str(y)[2:] for y in range(2017, 2025)]  # '17' to '24'
sessions = [("F", "M"), ("M", "J"), ("O", "N")]

for subject in subjects:
    for code in codes:
        for year in years:
            for D1, D2 in sessions:
                download_pastpaper(subject, code, D1, D2, year)
