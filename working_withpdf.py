from pypdf import PdfReader
import os
import pdfplumber
from tabula import read_pdf
import pandas as pd
#reader = PdfReader(r"C:\Users\isarivelan.mani\OneDrive - Wood PLC\Documents\Git\mani\sample.pdf")
#print(len(reader.pages))

#page = reader.pages[0]

#print(page.extract_text())

""" for i in range(len(reader.pages)):
    page = reader.pages[i]
    print(page.extract_text()) """

table_data = []
with pdfplumber.open (r"C:\Users\isarivelan.mani\OneDrive - Wood PLC\Documents\Git\mani\sample.pdf") as f:
    for i in f.pages:
        table_data = i.extract_tables()
        print(table_data)
        df1 = pd.DataFrame(table_data[0][1:], columns=table_data[0][0])
        df1.to_excel('pdf_extracted_table1.xlsx', index = False)
     

    
    
    print(df1)
    
       
       
        
