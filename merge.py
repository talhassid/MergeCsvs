import csv
import sys


class MergeCsvs():
    data = {}
    headers_set = set()  # set of headers in the final csv file
    ID_HEADER = 'id'

    def update_data_of_single_file(self, input_file):
        """
        Update self.data with the data of input file.

        :param input_file: csv file
        :return: None
        """
        with open(input_file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            current_csv_headers = next(reader,None)
            id_index = current_csv_headers.index(self.ID_HEADER)
            # for line in csv file
            for row in reader:
                current_id = row[id_index]
                if current_id not in self.data.keys():
                    self.data.update({current_id: {}})
                # for cell in line
                for counter, current_cell_value in enumerate(row):
                    current_header = current_csv_headers[counter]
                    if current_header == self.ID_HEADER:
                        continue
                    self.headers_set.add(current_header)
                    self.data[current_id].update({current_header: current_cell_value})

    def merge_csvs(self, csvs):
        """
        Merge all the csv files in the list to the self.data structure.

        :param csvs: list of names of csv files
        :return: None
        """
        for csv_file in csvs:
            self.update_data_of_single_file(input_file=csv_file)

    def add_empty_fields(self):
        """
        For each ID add missing headers with ' '
        :return: None
        """
        for id, current_id_data in self.data.items():
            if set(current_id_data.keys()) == self.headers_set:
                continue
            missing_headers = (self.headers_set - set(current_id_data.keys()))
            for header in missing_headers:
                self.data[id].update({header: ' '})

    def write_data_to_output_file(self, output_file):
        """
        Write the data in the self.data structure to a final csv.

        :param output_file: path of the output file
        :return: None
        """
        self.add_empty_fields()
        headers_list = list(self.headers_set)
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            header = [self.ID_HEADER] + headers_list
            writer.writerow(header)
            for id, current_id_data in self.data.items():
                line = [id]
                for header in headers_list:
                    line.append(current_id_data[header])
                writer.writerow(line)


if __name__ == '__main__':
    input_str = sys.argv[1:]
    merger = MergeCsvs()
    csv_list = input_str [1:]
    output_file = input_str[0]
    merger.merge_csvs(csv_list)
    merger.write_data_to_output_file(output_file)
