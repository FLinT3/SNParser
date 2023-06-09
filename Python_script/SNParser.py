import requests
import pandas as pd
import re
from bs4 import BeautifulSoup as BS


def table_t_finder(info_main_table):
    global Gene
    Gene = ""
    for paragraph in info_main_table.find_all("tr"):
        columns = paragraph.find_all("td")
        if len(columns) > 1:
            column1_text = columns[0].get_text().strip()
            column2_text = columns[1].get_text().strip()

            # Save info about Gene
            if column1_text == "Gene":
                Gene = column2_text

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

# Reading SNP_id
SNP_id = open(r'D:\Project_test\SNP_identificators.txt', 'r')
listid = SNP_id.read().splitlines()
list_of_ID = []
for i in listid:
    list_of_ID.extend(i.split(', '))

# Reading the "raw" vcf and remove the spaces (Optional)
vcf_inp = open('D:\Project_test\snp_python.txt', "r")
vcf_out = open('D:\Project_test\snp_python_mod.txt', "w")
for line in vcf_inp:
   new_line = line.replace('\t', ' ')
   vcf_out.write(new_line)
vcf_inp.close()
vcf_out.close()

with open('D:\Project_test\snp_python_mod.txt', 'r') as infile, open('D:\Project_test\snp_python_sorted.txt', 'w') as outfile:
    for line in infile:
        if any(word in line for word in list_of_ID):
            outfile.write(line)

# Remove trash (; and etc.)
with open('D:\Project_test\snp_python_sorted.txt', 'r') as infile, open('D:\Project_test\snp_python_sd.txt', 'w') as outfile:
    for line in infile:
        line = re.sub(';.*? ', ' ', line)
        outfile.write(line)

line1 = "Chr Coord SNP_ID Before_mut After_mut Quality Other_inf(e.g.0/1-heterozygote)\n"
filename = 'D:\Project_test\snp_python_sd.txt'
def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

line_prepender(filename, line1)

print("Скоро начнем")
xe = 0

# BIG FOR!
for i in list_of_ID:

    # SNPedia parsing
    snp_id = i
    url = "https://www.snpedia.com/index.php/" + snp_id  # Request to SNPpedia with our SNP

    # Page request and HTML analysis using BeautifulSoup
    response = requests.get(url)
    soup = BS(response.text, "html.parser")

    # Adding the desired tag
    info_div = soup.find("div", {"class": "mw-content-ltr"})
    info_main_table = soup.find("div", {"class": "aside-right col-sm-4"})

    # Extracting information
    try:
        div_p_finder(info_div)
    except:
        gene_info = "<b>NOT FOUND INFORMATION ABOUT GENE :(</b>"

    try:
        table_t_finder(info_main_table)
    except:
        Gene = "LOL :("
        print("ATTANTION!")

    # Remove PMID
    if gene_info not in "<b>NOT FOUND INFORMATION ABOUT GENE :(</b>":
        gene_info = re.sub(r'\[.*?\]', ' ', gene_info)

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

    # Writing in html file
    info_sum = soup.find_all("table", class_="sortable")
    with open(f"D:\Project_test\HTMLs\{snp_id}.html", "w", encoding="utf-8") as table:
        if Gene:
            table.write(f"<b>Gene - {Gene}</b>\n")
        if info_sum == []:
            info_sum = "<b>Sorry, we didn't find information about significance of this SNP :(</b><br>(You may just scip this snip)"
        table.write('<br><br>' + str(info_sum) + '<br><br>' + gene_info + '<br><br>' + html_report + '<br></br>')
        table.write("____________________________________________" * 6 + '<br><br><br><br>')
    xe += 1
    print(str(xe) + 'й' + ' готов')

print("Готовим финальный репорт...")

# Объединяем html файлы
html_dir = "D:\Project_test\HTMLs\\"
combined_html = ''
html_files = []

for j in list_of_ID:
    html_files.append(j + ".html")

for file in html_files:
    with open(html_dir + file, 'r') as fi:
        soup = BS(fi.read(), 'html.parser')
    combined_html += str(soup)

with open('D:\Project_test\combined.html', 'w', encoding="utf-8") as fi:
    fi.write(combined_html)

print("Ready!\thank you for using SNParser!")
