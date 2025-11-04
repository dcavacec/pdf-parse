# path: extract_uniform_values.py
import pdfplumber
import re
import json
import csv

def extract_uniform_values(pdf_path, json_out="values.json", csv_out="values.csv"):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            # Normalize text
            for line in text.splitlines():
                clean = re.sub(r'\s+', ' ', line.strip())
                if not clean:
                    continue

                # Match "Label: Value" or "Label  Value"
                match = re.match(r"(.+?)[\s:]{2,}(.+)", clean)
                if not match:
                    # If no clear split, store as single value
                    data.append({"field": None, "value": clean})
                else:
                    data.append({
                        "field": match.group(1).strip(),
                        "value": match.group(2).strip()
                    })

    # Export JSON
    with open(json_out, "w", encoding="utf-8") as jf:
        json.dump(data, jf, indent=2, ensure_ascii=False)

    # Export CSV
    with open(csv_out, "w", encoding="utf-8", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=["field", "value"])
        writer.writeheader()
        writer.writerows(data)

    return data

if __name__ == "__main__":
    extract_uniform_values("data/pdf_example.pdf")
