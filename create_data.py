import csv
import glob
from math import floor
import os

def create_data(file_list, type):
    print("Creating new data...")

    csv.register_dialect("myDialect", delimiter="\t")
    # i = 1
    with open(os.path.join(f"new_data/{type}.csv"), "w", newline="", encoding="utf-8") as myFile:
        writer = csv.writer(myFile, dialect='myDialect')
        rows = []
        for filename in file_list:
            print("Filename: ", filename)
            with open(filename, 'r', encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    myData = line.split("\t")
                    if len(myData) == 1 or myData[0] in ["<s>", "</s>"]:
                        if myData[0] == "</s>":
                            rows.append([])
                        else:
                            pass
                    else:
                        rows.append(myData[:-1])
                # if i == 50:
                #     break
            f.close()
            # i += 1
        writer.writerows(rows)
    myFile.close()

    print("Finished.")

if __name__ == "__main__":
    file_list = glob.glob(os.path.join("data/raw_data/train", "*.txt"))
    threshold = floor(len(file_list) * 0.7)
    train_list = file_list[:threshold]
    valid_list = file_list[threshold:]
    create_data(train_list, "train")
    create_data(valid_list, "valid")