import json

class Join:
    file = "dataJoined.json"
    files = ["avendre.json","doorInsider.json", "immoRegion.json", "maisonAppart.json", "ouest.json"]

    def writeData(self,listData, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("[\n")
            for ligne in listData:
                data = json.dumps(ligne, ensure_ascii=False)
                file.write(data)
                file.write(",\n")
            file.write("]\n")

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
        self.writeData(data, self.file)

if __name__ == '__main__':
    Join().main()
