import fitz  # PyMuPDF
import pandas as pd

from nebih_data import find_legal_documents
from gui import GUI
from scrape import check_eurlex_docs
import csv

# Get the food legislation list in pdf from the NÉBIH website
# NEBIH_URL = "https://portal.nebih.gov.hu/-/elelmiszer-jogszabalyok-jegyzeke"
# get_nebih_data(url=NEBIH_URL)

# Find the food legislation list from the file explorer
if __name__ == "__main__":
    gui = GUI()
    filepath = gui.filepath

    if filepath:
        pdf_file = fitz.open(filepath)
        eurlex_raw, netjogtar = find_legal_documents(pdf=pdf_file)

        # Removing duplicates from the Eurlex list
        # eurlex = []
        # for link in eurlex_raw:
        #     if link not in eurlex:
        #         eurlex.append(link)
        # short_eurlex = eurlex[1:1]

        # Or use these 5 regulations to see some problematic results
        list_of_everything = ["https://eur-lex.europa.eu/legal-content/HU/TXT/?uri=CELEX:32020R2236",
                              "https://eur-lex.europa.eu/eli/reg/2004/854/oj",
                              "https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=celex%3A32004R0882",
                              "https://eur-lex.europa.eu/legal-content/HU/TXT/?uri=uriserv%3AOJ.L_.2023.234.01.0196.01.HUN&toc=OJ%3AL%3A2023%3A234%3ATOC",
                              "https://eur-lex.europa.eu/eli/reg/2007/1234/oj"]

        # Call the checker function and create the repealed and modified list from the scraped data
        result = check_eurlex_docs(list_of_everything)
        df = pd.DataFrame(result)

        repealed_regulations = []
        modified_regulations = []
        for i, row in df.iterrows():
            if not row['in_force']:
                repealed_regulations.append(row)
            elif not row['is_up_to_date']:
                modified_regulations.append(row)
        # print(f"Not in force: {repealed_regulations}")
        # print(f"Has been modified: {modified_regulations}")

        # Open the 2nd window of the GUI with the 2 tabs
        gui.show_evaluation(repealed_list=repealed_regulations, modified_list=modified_regulations)

        # For testing, create a csv
        # with open("data/scraped_data.csv", 'w', newline='', encoding="utf-8") as file:
        #     headers = result[0].keys()
        #     csv_writer = csv.DictWriter(file, fieldnames=headers)
        #     csv_writer.writeheader()
        #     csv_writer.writerows(result)

        gui.run()

