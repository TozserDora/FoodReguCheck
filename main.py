from nebih_data import get_nebih_data, find_legal_documents
from scrape import check_eurlex_docs
import fitz  # PyMuPDF

#Get the list of food legislations in pdf from the NÉBIH website
NEBIH_URL = "https://portal.nebih.gov.hu/-/elelmiszer-jogszabalyok-jegyzeke"
get_nebih_data(url=NEBIH_URL)

# Or use your own existing file from the data folder when creating pdf_file

# Create the lists for the 2 websites
pdf_file = fitz.open("data/nebih_collection.pdf")
eurlex_raw, netjogtar = find_legal_documents(pdf=pdf_file)

# Removing duplicates from the Eurlex list
eurlex = []
for link in eurlex_raw:
    if link not in eurlex:
        eurlex.append(link)

# Make it shorter for testing
short_eurlex = eurlex[10:15]

# Or use these 3 regulations to see the 3 types of result
list_of_everything = ["https://eur-lex.europa.eu/legal-content/HU/TXT/?uri=CELEX:32020R2236",
                      "https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=celex%3A32004R0882",
                      "https://eur-lex.europa.eu/legal-content/HU/TXT/?uri=uriserv%3AOJ.L_.2023.234.01.0196.01.HUN&toc=OJ%3AL%3A2023%3A234%3ATOC"]

# Call the checker function
result = check_eurlex_docs(list_of_everything)

# Make them a bit more legible
for doc in result:
    print(doc)
















