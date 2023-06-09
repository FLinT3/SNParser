from bs4 import BeautifulSoup as BS
import requests
from html.parser import HTMLParser
import pandas as pd
import numpy as np
import re

# A little more file preprocessing
# SNP selecting
IDs = open(r'D:\Project_test\SNP_identificators.txt', mode='r')
g = IDs.read().splitlines()
search_words = []
for i in g:
   search_words.extend(i.split(', '))

with open('D:\Project_test\snp_python_mod.txt', 'r') as infile, open('D:\Project_test\snp_python_sorted.txt', 'w') as outfile:
    for line in infile:
        if any(word in line for word in search_words):
            outfile.write(line)

# Remove trash (; and etc.)
with open('D:\Project_test\snp_python_sorted.txt', 'r') as infile, open('D:\Project_test\snp_python_sd.txt', 'w') as outfile:
        line = re.sub(';.*? ', ' ', line)
        outfile.write(line)

# Reading the vcf and remove the spaces (Optional)
vsf_inp = open('D:\Project_test\snp_python.txt', "r")
vsf_out = open('D:\Project_test\snp_python_mod.txt', "w")
for line in vsf_inp:
   new_line = line.replace('\t', ' ')
   vsf_out.write(new_line)

vsf_inp.close()
vsf_out.close()



# Reading SNP_id
SNP_id = open(r'D:\Project_test\SNP_identificators.txt', 'r')
listid = SNP_id.read().splitlines()
list_of_ID = []
for i in listid:
    list_of_ID.extend(i.split(', '))

# BIG cycle FOR!
xe = 0
for i in list_of_ID:
    # SNPedia parsing
    snp_id = i
    url = "https://www.snpedia.com/index.php/" + snp_id

    # Page request and HTML analysis using BeautifulSoup
    response = requests.get(url)
    soup = BS(response.text, "html.parser")

    # Adding the desired tag
    info_div = soup.find("div", {"class": "mw-content-ltr"})
    info_main_table = soup.find("div", {"class": "aside-right col-sm-4"})

    # Extracting information
    def div_p_finder(info_div):
        global disease_info
        global gene_info
        disease_info = ""
        gene_info = ""
        j = 0
        for paragraph in info_div.find_all("p"):
            text = paragraph.get_text()
            if j >= 7:
                break
            elif "gene" in text.lower():
                gene_info += text + "\n"
                j += 1

    try:
        div_p_finder(info_div)
    except:
        gene_info = "No information found about the gene :("
    Gene = ""

    # Iterate through the main table
    for paragraph in info_main_table.find_all("tr"):
        columns = paragraph.find_all("td")
        if len(columns) > 1:
            column1_text = columns[0].get_text().strip()
            column2_text = columns[1].get_text().strip()

            # Save information about the Gene column
            if column1_text == "Gene":
                Gene = column2_text

    # Delete [PMID]
    if gene_info not in "No information found about the gene:(":
        gene_info = re.sub(r'\[.*?\]', ' ', gene_info)

    # We output the corresponding information from VCF
    vcf = open('D:\Project_test\snp_python_sd.txt', "r")
    df = pd.read_csv(vcf, delimiter=' ')


    def pars_df(df):
        for index, row in df.iterrows():
            time_value = row[2]
            if time_value == snp_id:
                return row

    report = pars_df(df)
    report = pd.DataFrame(report)
    html_report = report.to_html()

    # Write to an html file
    info_sum = soup.find_all("table", class_="sortable")
    with open(f"D:\Project_test\HTMLs\{snp_id}.html", "w", encoding="utf-8") as table:
        if Gene:
            table.write(f"<b>Gene - {Gene}</b>\n")
        table.write('<br><br>' + str(info_sum) + '<br><br>' + gene_info + '<br><br>' + html_report + '<br><br><br><br>')
        table.write("-------------------------------------------------------------------------------------------")
    xe += 1
    print(str(xe) + ' ready')

print("Preparing the final report...")

# Combining html files
html_dir = "D:\Project_test\HTMLs\\"
combined_html = ''
html_files = []

for j in list_of_ID:
    html_files.append(j + ".html")

for file in html_files:
    with open(html_dir + file, 'r') as f:
        soup = BS(f.read(), 'html.parser')

    combined_html += str(soup)

with open('D:\Project_test\combined.html', 'w') as f:
    f.write(combined_html)

print("Ready!\thank you for using SNParser!")