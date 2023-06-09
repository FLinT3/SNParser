# SNParser

<img src="https://s1.gifyu.com/images/tumblr_p3hky5x2Ce1tpia39o1_500.gif" width="20%">

# About

This is a small script, which can help you to annotate your SNPs. The program take on input your SNP-ID from the VCF file and generated a report based on SNPedia (https://www.snpedia.com/) data.

# Steps

### 1. File preparation
Firstly, we need to convert the file for reading. To do this, filter out the unique SNP-IDs by bash:
```bash
# Filtering out the necessary columns in the original vcf file
egrep -v '^#|^$' snps_snpsift_clinvar.vcf | cut -f 1-6,10 > snp_python.txt

# Select the identifiers of SNPs
awk '($32!="-")' snps_snpsift_clinvar.txt | grep risk_factor | cut -f 1-3,19 | sort | uniq > sorted_SNP.txt
cut -f 3 sorted_SNP.txt | uniq > zzz.txt
cut -d ';' -f1 zzz.txt > SNP_identificators.txt
```
*Note: if you wont to select exect clinically significant, you can use the Clean Var database and download vcf with ClinVar variants (https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz). For this you also shode to download SnpSift (https://pcingola.github.io/SnpEff/)*

```bash
java -jar SnpSift.jar annotate clinvar.vcf snps.vcf > snps_snpsift_clinvar.vcf 
```
