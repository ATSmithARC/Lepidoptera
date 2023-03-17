import csv
import json

input_filename = "C://Users//ATSmi//Desktop//cph_species.csv"
output_filename = "C://Users//ATSmi//Desktop//cph_species_coulmn2.csv"
output_filename_cleaned = "C://Users//ATSmi//Desktop//cph_species_coulmn2_cleaned.csv"
output_filename_cleaned_sorted = "C://Users//ATSmi//Desktop//cph_species_coulmn2_cleaned_sorted.csv"
output_filename_cleaned_sorted_unique = "C://Users//ATSmi//Desktop//cph_species_coulmn2_cleaned_sorted_unique.csv"
output_json = "C://Users//ATSmi//Desktop//cph_species.json"

def extract_column_and_write_to_csv(input_filename, output_filename):
    with open(input_filename, newline='', encoding="utf8") as input_csv_file:
        reader = csv.reader(input_csv_file, delimiter='\t')
        column = []
        row_count = 0
        for row in reader:
            row_count = row_count + 1
            if (row[19] != ""):
                column.append(row[19])
            else:
                column.append(row[1])

    print(row_count)
    with open(output_filename, 'w', newline='', encoding="utf8") as output_csv_file:
        writer = csv.writer(output_csv_file)
        for value in column:
            writer.writerow([value])

def remove_numbers(input_filename, output_filename):
    with open(input_filename, newline='', encoding="utf8") as input_csv_file:
        reader = csv.reader(input_csv_file)
        with open(output_filename, 'w', newline='', encoding="utf8") as output_csv_file:
            writer = csv.writer(output_csv_file)
            for row in reader:
                new_row = []
                for value in row:
                    result = ''.join([i for i in value if not i.isdigit()])
                    new_row.append(result.replace(',', ''))
                writer.writerow(new_row)

def sort_first_column(input_filename, output_filename):
    with open(input_filename, 'r', encoding="utf8") as input_csv_file:
        reader = csv.reader(input_csv_file)
        data = list(reader)
        
    data.sort(key=lambda row: row[0])
        
    with open(output_filename, 'w', newline='', encoding="utf8") as output_csv_file:
        writer = csv.writer(output_csv_file)
        writer.writerows(data)

def csv_to_json(input_filename, output_filename):
    with open(input_filename, 'r', encoding="utf8") as input_csv_file:
        reader = csv.reader(input_csv_file)
        array = []
        for row in reader:
            array.append(row[0])
    
    with open(output_json, 'w', encoding="utf8") as file:
        json.dump(array, file)

def remove_duplicates(input_filename, output_filename):
    seen = set()
    with open(input_filename, 'r', encoding="utf8") as infile, open(output_filename, 'w', newline='', encoding="utf8") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            if row[0] not in seen:
                seen.add(row[0])
                writer.writerow(row)

    

#extract_column_and_write_to_csv(input_filename, output_filename)
#remove_numbers(output_filename, output_filename_cleaned)
#sort_first_column(output_filename_cleaned, output_filename_cleaned_sorted)
#remove_duplicates(output_filename_cleaned_sorted,output_filename_cleaned_sorted_unique)
csv_to_json(output_filename_cleaned_sorted_unique, output_json)
