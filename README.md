# BV-BRC Viral Data Extractor

This Python script is specifically designed for extracting and processing viral genomic, protein, nucleotide, and feature data from BV-BRC. The tool handles the unique structure of BV-BRC viral family files, enabling efficient data extraction, redundancy handling, and organization.

---

## Features

- **Download Viral Family Files**: Automatically download files like `.fna`, `.faa`, `.ffn`, and `.features.tab` for viral genomes from BV-BRC based on the family name.
- **Custom Output Directory**: User-defined output directory for organizing the extracted data.
- **Extract Specific Data**: Support for extracting genome (`.fna`), protein (`.faa`), nucleotide features (`.ffn`), and tabular features (`.features.tab`).
- **Handle Redundancies**: Combines multiple contigs for the same genome ID into one file.
- **Logging**: Logs all activities, including downloaded and failed genome IDs.
- **Run as Background Process**: Easily use `nohup` to run the script in the background with logs.

---

## Requirements

- Python 3.6+
- Modules: `argparse`, `os`, `sys`, `re`, `subprocess`

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/bvbrc-viral-data-extractor.git
   cd bvbrc-viral-data-extractor
   ```

2. **Ensure the required Python version is installed.**

3. **Make the script executable**:
   ```bash
   chmod +x extract_bvbrc_viral_data.py
   ```

---

## Usage Examples

### 1. Basic Command (Using Downloaded Files)
If the viral family files are already downloaded:
```bash
python extract_bvbrc_viral_data.py --genome_list genome_list.txt --output_dir my_output --fna --faa --ffn --features
```

### 2. Download Viral Family Files Automatically
If files like `.fna`, `.faa`, `.ffn`, or `.features.tab` are not available locally, the script can download them:
```bash
python extract_bvbrc_viral_data.py --genome_list genome_list.txt --output_dir my_output --family_name Pneumoviridae --fna --faa --ffn --features
```

### 3. Run in Background with Logs
```bash
nohup python extract_bvbrc_viral_data.py --genome_list genome_list.txt --output_dir my_output --family_name Pneumoviridae --fna --faa --ffn --features > extract_bvbrc_viral_data.log 2>&1 &
```

---

## Arguments

- `--genome_list`: Path to the file containing the list of genome IDs (required).
- `--output_dir`: Directory to save the extracted files (default: `output`).
- `--family_name`: Viral family name to download files (optional).
- `--fna`: Extract genome files (`.fna`).
- `--faa`: Extract protein files (`.faa`).
- `--ffn`: Extract nucleotide feature files (`.ffn`).
- `--features`: Extract tabular feature files (`.features.tab`).
-  For help, ```bash
   python extract_bvbrc_data.py --help
        ```
---

## Example Input File (genome_list.txt)

```plaintext
162145.1193
162145.1195
162145.1196
38525.15
```

---

## Output Structure

The script creates the following directory structure based on the `--output_dir` argument:

```
my_output/
├── fna/
│   ├── 162145.1193.fna
│   ├── 162145.1195.fna
│   └── ...
├── faa/
│   ├── 162145.1193.faa
│   ├── 162145.1195.faa
│   └── ...
├── ffn/
│   ├── 162145.1193.ffn
│   ├── 162145.1195.ffn
│   └── ...
├── features/
│   ├── 162145.1193.features.tab
│   ├── 162145.1195.features.tab
│   └── ...
└── logs/
    ├── success.log
    └── error.log
```

---

## Logs

- **`success.log`**: Lists all successfully extracted genome IDs.
- **`error.log`**: Lists genome IDs that failed to download or extract.

---

## Citation
If you are using the extract_bvbrc_viral_data.py script, please cite it as follows:

Sharma, V. (2025). extract_bvbrc_viral_data.py [Python script]. Retrieved from [https://github.com/vsmicrogenomics/extract_bvbrc_viral_data]


---

## Acknowledgments

We would like to extend our sincere gratitude to the Bacterial and Viral Bioinformatics Resource Center (BV-BRC), formerly known as PATRIC, for making their comprehensive database of bacterial and viral genomic data accessible to the research community.
