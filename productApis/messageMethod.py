import requests
import json
import pymongo
import pandas as pd

df = pd.read_excel('tada.xlsx')


con = pymongo.MongoClient("localhost", 27017)
# database name
db = con['NazAf']
# collection for chat_users
chat_user_table = db['chat_users']




month_dic = {}
month_dic[1] = 'Jan'
month_dic[2] = 'Feb'
month_dic[3] = 'Mar'
month_dic[4] = 'Apr'
month_dic[5] = 'May'
month_dic[6] = 'Jun'
month_dic[7] = 'Jul'
month_dic[8] = 'Aug'
month_dic[9] = 'Sep'
month_dic[10] = 'Oct'
month_dic[11] = 'Nov'
month_dic[12] = 'Dec'

# CHECK THE EMPLOYE CODE IN THE FILE
def check_em_code_file(employe_code):
    data = df.where(df['Employee Code']==int(employe_code)).dropna()
    if data.empty:
        return False
    else:
        return True




def create_employe_data(dataframe):
    return_string = ""
    for index in range(len(dataframe)):

        employe_name = dataframe.iloc[index]['Employee Name']
        # reciving_date = dataframe.iloc[index]['DATE OF RECEIVING']
        month = dataframe.iloc[index]['Month']
        claim_amount = dataframe.iloc[index][' Claim amount']
        grand_total = dataframe.iloc[index]['Grand Total']
        deduction = dataframe.iloc[index]['Deduction']
        reason = dataframe.iloc[index]['REASON OF DEDUCTIONS'] 
        return_string =return_string+ "--------------------------------------------------\n                   DETAILS                      \n--------------------------------------------------\n"

        # return_string = return_string + " Employee Name             :  " + employe_name  + "\n Date Of Receiving             :  " + str(reciving_date) + "\n Month                               : " + str(month)
        return_string = return_string + " Employee Name             :  " + employe_name  + "\n Month                               : " + str(month)

        return_string = return_string + "\n Claim amount                 :  " + str(claim_amount)+ "\n Amount Paid                   :  " + str(grand_total)+ "\n Deduction                        :  " + str(deduction)
        return_string = return_string +"\n Reason Of Deductions  :  \n" + reason +"\n"


    return return_string


# CHECK THE MONTH AND YEAR
def check_month_year(text):
    try:
        text = text.split('/')
        month = int(text[0])
        year = int(text[1])
        string = month_dic[month]+"-" + str(year)[-2:]
        return {'status':True, 'string':string}
    except Exception as e:
        # print(e)
        return {'status':False, 'string':'' }

def check_employee_code_return_data(employe_code, month):
    data = df.where((df['Employee Code']==int(employe_code) )& (df['Month']==str(month))).dropna()
    if data.empty:
        return "Data is Not available for the given month."
    else:
        return create_employe_data(data)


def send_message(number, message):
    url = "https://graph.facebook.com/v14.0/103634132488392/messages"
    headers = {"Authorization":""}
    headers['Content-Type'] = "application/json"
    # data = { "messaging_product": "whatsapp", "to": number,"type": "template", "template": { "name": "hello_world", "language": { "code": "en_US" } } }
    # print(data)
    data = {
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": number,
  "type": "text",
  "text": { 
    "preview_url": False,
    "body": message
  }
}

    res = requests.post(url, headers=headers, data=json.dumps(data, indent=4))


def conversation(number , message_text):
    # find the user in table
    chat_user  = chat_user_table.find_one({'user_number':number})
    chat_state = "0"




    if chat_user:
        chat_state = chat_user.get('chat_state')
    else:
        chat_user_table.insert_one({"user_number":number, 'chat_state':"0"})
    

        #Cancel the chat or restart
    if message_text in ['cancel', '/cancel', 'stop','restart', 'Cancel', 'Stop', 'Restart']:
        chat_user_table.update_one({"user_number":number}, {"$set":{'chat_state':"0", "em_code":""}})
        return "Bye! I hope we can talk again some day."


    # process the message
    # START CHAT
    if chat_state == "0":
        if message_text in ['hi', 'hello', 'Hi', 'Hello'] : 
            return_text = "hi, i am TADA BOT, I will hold a conservation with you.\n You can stop conversion by sending stop. \n what is your employee code?"
            chat_user_table.update_one({'user_number':number}, {"$set":{"chat_state":"1"}})
            return return_text
        else:
            return_text = "For satrting the conversation send hi "
            return return_text

    # CHECK FOR THE EMPLOYEE
    elif chat_state == "1":
        if message_text.isnumeric():
            employee_status = check_em_code_file(message_text)
            if employee_status:
                chat_user_table.update_one({'user_number': number}, {"$set":{"em_code": message_text, "chat_state" : "2"}})
                return_text = "Enter  month and year in mm/yy Format.\nExample: 03/17"
                return return_text
            else:
                return "Invalid Employee Code"

        else:
            return_text = "Employee Code Must Be a Number"
            return return_text

    # CHECK THE DATE AND RETURN DATA
    elif chat_state =="2":
        month_status = check_month_year(message_text)
        if month_status['status']:
            employe_data = check_employee_code_return_data(chat_user['em_code'], month_status['string'])
            return employe_data
        else:
            return "Incorrect Format"


    return "working on it"
    # Store Employee code if correct
    # SECOND CHECK THE EMPLOYEE CODE IF CORRECT MOVE TO NEXT ASK FOR MONTH AND YEAR
    # IF CORRECT RETURN THE DATA , ASK FOR STOPING THE CONVERSATION.
