import csv


def csv_dict_writer(path, fieldnames, data):
    """
    Writes a CSV file using DictWriter
    """
    with open(path, "w", newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter='|', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
