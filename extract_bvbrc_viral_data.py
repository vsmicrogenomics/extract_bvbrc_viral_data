import os
import subprocess
import argparse


def create_directories(output_dir):
    os.makedirs(output_dir, exist_ok=True)


def download_family_files(family_name):
    files = {
        "fna": f"{family_name}.fna",
        "faa": f"{family_name}.PATRIC.faa",
        "ffn": f"{family_name}.PATRIC.ffn",
        "features": f"{family_name}.PATRIC.features.tab",
    }
    for key, filename in files.items():
        if not os.path.exists(filename):
            print(f"Downloading {filename}...")
            subprocess.run(
                [
                    "wget",
                    f"ftp://ftp.bvbrc.org/viruses/{filename}",
                    "-O",
                    filename,
                ],
                check=True,
            )
    return files


def extract_sequences(input_file, genome_list_file, output_dir, extension, log_file):
    with open(genome_list_file, "r") as gl:
        genome_ids = [line.strip() for line in gl if line.strip()]

    successfully_downloaded = []
    not_downloaded = []
    genome_data = {genome_id: [] for genome_id in genome_ids}

    with open(input_file, "r") as infile:
        current_header = None
        current_sequence = []

        for line in infile:
            line = line.strip()
            if line.startswith(">"):  # Header line
                if current_header and current_sequence:
                    genome_id = extract_genome_id(current_header)
                    if genome_id in genome_data:
                        genome_data[genome_id].append(
                            f"{current_header}\n{''.join(current_sequence)}"
                        )
                current_header = line
                current_sequence = []
            else:
                current_sequence.append(line)

        # Save the last sequence
        if current_header and current_sequence:
            genome_id = extract_genome_id(current_header)
            if genome_id in genome_data:
                genome_data[genome_id].append(
                    f"{current_header}\n{''.join(current_sequence)}"
                )

    for genome_id, sequences in genome_data.items():
        if sequences:
            output_path = os.path.join(output_dir, f"{genome_id}.{extension}")
            with open(output_path, "w") as out_file:
                out_file.write("\n".join(sequences))
            successfully_downloaded.append(genome_id)
        else:
            not_downloaded.append(genome_id)

    with open(log_file, "w") as log:
        log.write("Successfully Extracted IDs:\n")
        log.write("\n".join(successfully_downloaded) + "\n")
        log.write("\nNot Found IDs:\n")
        log.write("\n".join(not_downloaded) + "\n")


def extract_features(input_features_file, genome_list_file, output_dir, log_file):
    with open(genome_list_file, "r") as gl:
        genome_ids = [line.strip() for line in gl if line.strip()]

    successfully_extracted = []
    not_found = []

    with open(input_features_file, "r") as features_file:
        header = features_file.readline().strip()
        genome_features = {genome_id: [] for genome_id in genome_ids}

        for line in features_file:
            line = line.strip()
            if not line:
                continue
            columns = line.split("\t")
            genome_id = columns[0]
            if genome_id in genome_features:
                genome_features[genome_id].append(line)

    for genome_id, features in genome_features.items():
        if features:
            output_path = os.path.join(output_dir, f"{genome_id}.features.tab")
            with open(output_path, "w") as out_file:
                out_file.write(header + "\n")
                out_file.write("\n".join(features) + "\n")
            successfully_extracted.append(genome_id)
        else:
            not_found.append(genome_id)

    with open(log_file, "w") as log:
        log.write("Successfully Extracted IDs:\n")
        log.write("\n".join(successfully_extracted) + "\n")
        log.write("\nNot Found IDs:\n")
        log.write("\n".join(not_found) + "\n")


def extract_genome_id(header):
    try:
        return header.split("|")[-1].strip(" ]")
    except IndexError:
        return ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract sequences and features from BV-BRC files.")
    parser.add_argument("--genome_list", help="File containing genome IDs", required=True)
    parser.add_argument("--output_dir", help="Output directory name", required=True)
    parser.add_argument("--family_name", help="Family name for downloading files", default=None)
    parser.add_argument("--fna_file", help="Path to the .fna file", default=None)
    parser.add_argument("--faa_file", help="Path to the .PATRIC.faa file", default=None)
    parser.add_argument("--ffn_file", help="Path to the .PATRIC.ffn file", default=None)
    parser.add_argument("--features_file", help="Path to the .PATRIC.features.tab file", default=None)
    parser.add_argument("--extract_types", nargs="+", choices=["fna", "faa", "ffn", "features"], default=["fna", "faa", "ffn", "features"], help="Types of data to extract (default: all)")

    args = parser.parse_args()

    genome_list = args.genome_list
    output_dir = args.output_dir
    family_name = args.family_name

    # Create base output directory
    create_directories(output_dir)

    # If family name is provided, download necessary files
    if family_name:
        downloaded_files = download_family_files(family_name)
        args.fna_file = args.fna_file or downloaded_files["fna"]
        args.faa_file = args.faa_file or downloaded_files["faa"]
        args.ffn_file = args.ffn_file or downloaded_files["ffn"]
        args.features_file = args.features_file or downloaded_files["features"]

    # Process each file type as per user selection
    if "fna" in args.extract_types and args.fna_file:
        create_directories(os.path.join(output_dir, "fna"))
        extract_sequences(args.fna_file, genome_list, os.path.join(output_dir, "fna"), "fna", os.path.join(output_dir, "fna_extraction_log.txt"))

    if "faa" in args.extract_types and args.faa_file:
        create_directories(os.path.join(output_dir, "faa"))
        extract_sequences(args.faa_file, genome_list, os.path.join(output_dir, "faa"), "faa", os.path.join(output_dir, "faa_extraction_log.txt"))

    if "ffn" in args.extract_types and args.ffn_file:
        create_directories(os.path.join(output_dir, "ffn"))
        extract_sequences(args.ffn_file, genome_list, os.path.join(output_dir, "ffn"), "ffn", os.path.join(output_dir, "ffn_extraction_log.txt"))

    if "features" in args.extract_types and args.features_file:
        create_directories(os.path.join(output_dir, "features"))
        extract_features(args.features_file, genome_list, os.path.join(output_dir, "features"), os.path.join(output_dir, "features_extraction_log.txt"))
