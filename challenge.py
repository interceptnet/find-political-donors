#open file
inFile = open("itcont.txt")

#read data
data = []
for line in inFile:
    i = line.split("|")

    #dictionary as data items
    new_i = {}
    new_i['CMTE_ID'] = i[0]
    new_i['ZIP_CODE'] = i[10][:5]
    new_i['TRANSACTION_DT'] = i[13]
    new_i['TRANSACTION_AMT'] = i[14]
    new_i['OTHER_ID'] = i[15]

    if new_i['CMTE_ID'] != '' and new_i['TRANSACTION_AMT'] != '' and new_i['OTHER_ID'] == '' :
        data.append(new_i)
inFile.close()


outFile = open('medianvals_by_zip.txt','w+')
ledger = []
for item in data:
    #check for existing matches in the ledger
    match = next( (entry for entry in ledger if entry['id'] == item['CMTE_ID'] and entry['zip'] == item['ZIP_CODE']), None)
    if match:
        #add transaction to ledger
        match['transactions'].append(item['TRANSACTION_AMT'])

        #calculate median and total
        total=0
        for amt in match['transactions']:
            total += round(float(amt))
        median = round(total/len(match['transactions']))

        val = ( item['CMTE_ID']+"|"+item['ZIP_CODE']+"|"+str(median)+"|"+str(len(match['transactions']))+"|"+str(total))

    else:
        #add transaction to ledger
        entry = {'id':item['CMTE_ID'],'zip':item['ZIP_CODE'],'transactions':[item['TRANSACTION_AMT']]}
        ledger.append(entry)

        val = item['CMTE_ID']+"|"+item['ZIP_CODE']+"|"+item['TRANSACTION_AMT']+"|1|"+item['TRANSACTION_AMT']

    outFile.write(val+'\n')
outFile.close()

outFile = open('medianvals_by_date.txt','w+')
ledger = []
for item in data:
    #check for existing matches in the ledger
    match = next( (entry for entry in ledger if entry['id'] == item['CMTE_ID'] and entry['date'] == item['TRANSACTION_DT']), None)
    if match:
        #add transaction to ledger
        match['transactions'].append(item['TRANSACTION_AMT'])

    else:
        #add transaction to ledger
        entry = {'id':item['CMTE_ID'],'date':item['TRANSACTION_DT'],'transactions':[item['TRANSACTION_AMT']]}
        ledger.append(entry)

        val = item['CMTE_ID']+"|"+item['TRANSACTION_DT']+"|"+item['TRANSACTION_AMT']+"|1|"+item['TRANSACTION_AMT']

#sort ledger by date, then by id
ledger.sort(key=lambda item:item['date'][4:]+item['date'][:4])
ledger.sort(key=lambda item:item['id'])
for entry in ledger:

    # calculate median and total
    total = 0
    for amt in entry['transactions']:
        total += round(float(amt))
    median = round(total / len(entry['transactions']))

    val = (entry['id']+"|"+entry['date']+"|"+str(median)+"|"+str(len(entry['transactions']))+"|"+str(total))
    outFile.write(val+'\n')
outFile.close()



