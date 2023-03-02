import json
import csv


class Join:
    files = ["avendre.json","doorInsider.json", "maisonAppart.json","immoRegion.json", "ouest.json"]

    def writeData(self,listData):
        print(listData[0])
        keys = listData[0].keys()

        with open('dataJoined.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(listData)

    def readFile(self, fileName):
        with open(fileName, encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    def joinData(self):
        listData = []
        for file in self.files:
            data = self.readFile(file)
            listData.append(data)
        return listData



    def main(self):
        data = self.joinData()
        data = sum(data, [])
        print(len(data))
        self.writeData(data)

if __name__ == '__main__':
    Join().main()
