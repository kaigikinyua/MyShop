import csv

class MyCsvFile:
    
    @staticmethod
    def readCSVFile(pathToFile):
        data=[]
        infile=open(pathToFile)
        reader=csv.reader(infile)
        for row in reader:
            data.append(row)
        infile.close()
        return data
    
    @staticmethod
    def writeCSVFile(pathToFile):
        pass
        #do some reaserch on csv.writer

    @staticmethod
    def removeCSVHeaders(data):
        return data[0],data[1:len(data)]

    @staticmethod
    def getColumn(headers=None,columnName='',data=[]):
        i=0
        headerIndex=0
        headerString=""
        for header in headers:
            if(header.lower()==columnName.lower()):
                headerIndex=i
                headerString=header
                break
            i=i+1
        columnData=[]
        for row in data:
            columnData.append(row[headerIndex])
        return headerString,columnData
    
    @staticmethod
    def getRow(data=[],rowIndex=0,removedHeaders=True):
        if(removedHeaders==False):
            h,data=MyCsvFile.removeHeaders(data)
        if(len(data)<=rowIndex):
            return data[rowIndex]
        else:
            print("Array out of bounds index")
        return None

    @staticmethod
    def createCsv(headers=[],data=[],autoIndexRows=True):
        csvData=[]
        if(autoIndexRows):
            if(len(headers)==len(data[0])):
                headers.insert('Index',0)
            rowIndex=1
            for row in data:
                row.insert(rowIndex,0)
                csvData.append(row)
            csvData.insert(headers,0)
        else:
            csvData.append(headers)
            csvData.append(data)
        return csvData
    
if __name__=="__main__":
    data=MyCsvFile.readCSVFile("./test.csv")
    headers,data=MyCsvFile.removeHeaders(data)
    bCodeHeader,bCodedata=MyCsvFile.getColumn(headers=headers,columnName="bar code",data=data)
    tagsHeader,tagsData=MyCsvFile.getColumn(headers=headers,columnName="TaGs",data=data)
    print(f'Column {bCodeHeader} data={bCodedata}')
    print(f'Column {tagsHeader} data={tagsData}')