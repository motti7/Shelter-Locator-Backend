import pandas as pd

xlsx_file = r"C:\Users\מוטי\Desktop\מקלט עכשיו\miklat server\shelters_ptk_with_coords.xlsx"

csv_file = r"C:\Users\מוטי\Desktop\מקלט עכשיו\miklat server\shelters_ptk_with_coords.csv"

df = pd.read_excel(xlsx_file, engine="openpyxl")

df.to_csv(csv_file, index=False, encoding="utf-8-sig")

print(f"XLSX הומר בהצלחה ל-CSV: {csv_file}")