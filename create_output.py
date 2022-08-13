import glob
import os
import csv
from predict import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pretrain_dir", default="outputs/", type=str,)
    parser.add_argument("--feat_dir", default=None, type=str)
    parser.add_argument("--max_seq_length", default=128, type=int)
    parser.add_argument("--batch_size", default=8, type=int)
    parser.add_argument("--cuda", default=True, type=bool)

    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() and args.cuda else "cpu")

    ner = NER(args.pretrain_dir, args.feat_dir, args.max_seq_length, args.batch_size, device)

    file_list = glob.glob(os.path.join("data/raw_data/test", "*.txt"))

    # i=1
    for filename in file_list:
        csv.register_dialect("myDialect", delimiter="\t")
        with open(os.path.join(f"outputs/test/{os.path.basename(filename)[:-4]}.csv"), "w", newline="", encoding="utf-8") as myFile:
            writer = csv.writer(myFile, dialect='myDialect')
            input_text = []
            text_data = []
            with open(filename, 'r', encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    myData = line.split("\t")
                    if len(myData) != 1 and myData[0] not in ["<s>", "</s>"]:
                        input_text.append(myData[0])
                    temp = myData[:-1]
                    temp.append(myData[-1].replace("\n",""))
                    text_data.append(temp)
            f.close()
            outputs = ner.predict(" ".join(input_text))
            print(outputs)
            rows = []
            k, m = 0, 0
            while k < len(text_data):
                if m < len(outputs) and text_data[k][0] == outputs[m][0]:
                    text_data[k].append(outputs[m][1])
                    m += 1
                elif len(text_data[k]) != 1 and text_data[k][0] not in ["<s>", "</s>"]:
                    text_data[k].append("O")
                if text_data[k][0] == "":
                    text_data[k] = []
                rows.append(text_data[k])
                k += 1
            writer.writerows(rows)
        myFile.close()
        # if i == 1:
        #     break

    file_list = glob.glob(os.path.join("outputs/test", "*.csv"))
    for filename in file_list:
        os.rename(filename, f"outputs/new_test/{os.path.basename(filename)[:-4]}.txt")