# coding=utf-8
import csv


def normalize_all_songs(in_file, out_file):
    with open(in_file, 'rb') as in_csv:
        with open(out_file, 'wb') as out_csv:
            reader = csv.reader(in_csv, delimiter=',', quotechar='"')
            writer = csv.writer(out_csv, delimiter=',', quotechar='"')
            i = 0
            for row in reader:
                if i == 0:
                    row = ['title'] + row[-3:]
                else:
                    row = [' - '.join(row[0:-3])] + map(int, row[-3:])
                writer.writerow(row)
                if i % 1000 == 0:
                    print i
                i += 1
            print i


def normalize_music_section(in_file, out_file):
    with open(in_file, 'rb') as in_csv:
        with open(out_file, 'wb') as out_csv:
            reader = csv.reader(in_csv, delimiter=',', quotechar='"')
            writer = csv.writer(out_csv, delimiter=',', quotechar='"')
            i = 0
            for row in reader:
                if i == 0:
                    row = ['id', 'cloudcast_id', 'track_id', 'position']
                else:
                    if 'NULL' in row[0:4]:
                        continue
                    row = map(int, row[0:4])
                writer.writerow(row)
                if i % 1000 == 0:
                    print i
                i += 1
            print i


if __name__ == '__main__':

    in_file = '/Users/Air/Documents/mixcloud/mixcloud_music_section.csv'
    out_file = '/Users/Air/Documents/mixcloud/music_section.csv'
    normalize_music_section(in_file, out_file)
