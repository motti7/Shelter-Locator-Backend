import pandas as pd
import json


excel_file_path = r"C:\Users\מוטי\Desktop\מקלט עכשיו\shelters_ptk_with_coords.xlsx"
json_file_path = r"C:\Users\מוטי\Desktop\מקלט עכשיו\shelters.json"

try:
    df = pd.read_excel(excel_file_path)

    if "מספר מקלט" in df.columns:
        df = df.drop(columns=["מספר מקלט"])

    records = df.to_dict(orient="records")

    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(records, json_file, ensure_ascii=False, indent=2)

    print(f"הקובץ נוצר בהצלחה ושמור בשם: {json_file_path}")

except FileNotFoundError:
    print(f"שגיאה: הקובץ '{excel_file_path}' לא נמצא. ודא שהקובץ נמצא באותה תיקייה עם הסקריפט.")
except Exception as e:
    print(f"אירעה שגיאה כללית: {e}")