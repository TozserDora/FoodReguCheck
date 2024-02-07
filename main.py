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
        eurlex = []
        for link in eurlex_raw:
            if link not in eurlex:
                eurlex.append(link)
        short_eurlex = eurlex[0:3]

        # Or use these 3 regulations to see the 3 types of result
        list_of_everything = ["https://eur-lex.europa.eu/legal-content/HU/TXT/?uri=CELEX:32020R2236",
                              "https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=celex%3A32004R0882",
                              "https://eur-lex.europa.eu/legal-content/HU/TXT/?uri=uriserv%3AOJ.L_.2023.234.01.0196.01.HUN&toc=OJ%3AL%3A2023%3A234%3ATOC"]

        # Call the checker function and create a csv from the scraped data
        result = check_eurlex_docs(list_of_everything)
        df = pd.DataFrame(result)
        repealed_regulations = []
        old_versions = []
        for i, row in df.iterrows():
            if row['in_force'] == False:  # Check if 'col' is equal to False
                repealed_regulations.append(row)
            elif row['is_up_to_date'] == False:
                old_versions.append(row)
        print(f"Not in force: {repealed_regulations}")
        print(f"Has been modified: {old_versions}")
        gui.show_evaluation(repealed=repealed_regulations, old=old_versions)


        # For testing, create a csv
        # with open("data/scraped_data.csv", 'w', newline='', encoding="utf-8") as file:
        #     headers = result[0].keys()
        #     csv_writer = csv.DictWriter(file, fieldnames=headers)
        #     csv_writer.writeheader()
        #     csv_writer.writerows(result)

        gui.run()

