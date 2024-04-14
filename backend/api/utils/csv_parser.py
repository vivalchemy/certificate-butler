import csv
import io


def parseCSV(File):
    # Open the file in text mode
    # with io.TextIOWrapper(f, encoding="utf-8") as text_file:
    reader = csv.reader(File.file.read().decode("utf-8").splitlines())

    print("Decoded")
    print("Printing rows")
    next(reader, None)
    data = []
    for row in reader:
        print(row)
        try:
            data.append({"name": row[0], "email": row[1]})
        except Exception as e:
            print(e)
    # print(data)
    print("exiting parser")
    return data
