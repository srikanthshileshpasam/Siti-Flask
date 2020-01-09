#!/usr/bin/env python
# coding: utf-8

# In[46]:


from datetime import datetime
from getpass import getpass
from cryptography.fernet import Fernet
import pandas as pd
import random

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    class Auth:
        def __init__(self, user, pwd, fer_key):
            self.user = user
            self.pwd = pwd
            self.fer_key = fer_key
    
    
        def credentials(self):
            with open("User_Details.txt", "rb") as file:
                data = file.readlines()
                file.close()
            
                x = False
                y = 0
                while x == False and y < len(data):
                    if (self.fer_key.decrypt(self.user) == self.fer_key.decrypt(data[y])) and (self.fer_key.decrypt(self.pwd) == self.fer_key.decrypt(data[y+1])):
                        x = True
                        return True
                    else:
                        y += 2
            
                if x == False:
                    return False
            
        
        def new_user(self):
            file = open("User_Details.txt", "ab")

            file.write(self.user)
            line = str(0) + "\n"
            file.write(line.encode('utf-8'))

            file.write(self.pwd)
            line = str(0) + "\n"
            file.write(line.encode('utf-8'))

            file.close()

            return 'User created successfully!'



    class Keys:
        def key_gen():
            key = Fernet.generate_key()

            file = open("Fernet_Key.txt", "wb")
            file.write(key)
            file.close()

            print('New key generated successfully!')


        def read_key():
            with open('Fernet_Key.txt', 'rb') as file:
                data = file.read()
                file.close()

            return data



    class LoadData:

        def __init__(self, agent_name, vc_number, receipt_number=None, package_name=None, amount_received=None, remarks_any=None):
            self.agent_name = agent_name
            self.vc_number = vc_number
            self.receipt_number = receipt_number
            self.package_name = package_name
            self.amount_received = amount_received
            self.remarks_any = remarks_any

            self.dir_path = "/Users/srikanthshileshpasam/Documents/GitHub/PSRK_CollectionAPP/Data/"
            self.master_file_name = 'TVR_Siti_Collection_Form_Master.csv'
            self.monthly_file_name = 'TVR_Siti_Collection_Form_Monthly.csv'


        def vc_check(self):
            vc_read = pd.read_csv(self.dir_path + self.master_file_name)

            data_df = pd.DataFrame(vc_read, columns = ['VC No', 'LCO ID', 'Name', 'Due Date', 'Cel 1'])

            vc_result = data_df["VC No"].isin([self.vc_number]) 
            data_df = data_df[vc_result]

            if data_df.empty == True:
                return False

            else:
                return data_df


        def file_open(self):    
            monthly_data = pd.read_csv(self.dir_path + self.monthly_file_name)

            class_call = DataEntry(monthly_data, self.dir_path, self.monthly_file_name)
            send_details = class_call.write_data(self.agent_name, self.vc_number, self.receipt_number, self.package_name, self.amount_received, self.remarks_any)

            return send_details




    class DataEntry:
        def __init__(self, monthly, dir_name, monthly_name):
            self.monthly = monthly
            self.dir_name = dir_name
            self.monthly_name = monthly_name


        def write_data(self, agent_id, vc, receipt, package, amount, rem):
            self.agent_id = agent_id
            self.vc = vc
            self.receipt = receipt
            self.package = package
            self.amount = amount
            self.rem = rem

            date_time = datetime.now().strftime('%d-%m-%y %H:%M')
            auto_bill_num = random.randint(10000,99999999) 
    #         need to develop


            self.monthly = self.monthly.append({'VC No':vc, 'Rec No':receipt, 'PKG':package, 'Recd Amt':amount, 'Coll Point':agent_id, 'Remarks':rem, 'Auto Bill No':auto_bill_num, 'Date':date_time}, ignore_index=True)

            print('\nSaving file..\n')

            self.monthly.to_csv(self.dir_name + self.monthly_name, index=False)

            return True




    # Keys.key_gen()


    login = int(input('\nWelcome!\nAre you an existing user or a new user?\n1) Existing user\n2) New user\n'))

    if login == 1:
        user_id = input('\nUsername: ')
        user_id_enc = user_id.encode()
        pwd = getpass('Password: ')
        pwd = pwd.encode()

        key_code = Keys
        code = key_code.read_key()

        key = Fernet(code)

        encrypted_pwd = key.encrypt(pwd)
        encrypted_id = key.encrypt(user_id_enc)

        user_auth = Auth(encrypted_id, encrypted_pwd, key)

        login_status = user_auth.credentials()


        if login_status == True:

            vc_num = input('\nEnter VC number:\n')
            while vc_num[0] != '0' and len(vc_num) > 10 and len(vc_num) < 5:
                vc_num = input('\nINVALID VC!\nTry again..\nEnter VC number:\n')

            start_program = LoadData(user_id, vc_num)
            vc_exist = start_program.vc_check()

            if isinstance(vc_exist, pd.DataFrame):
                print(f'\nVC details found.\nVerify customer details before proceeding.\n\n{vc_exist}')

                receipt_num = int(input('\nEnter Receipt number:\n'))
                while receipt_num > 99999:
                    receipt_num = int(input('\nINVALID RECEIPT!\nTry again..\nEnter Receipt number:\n'))

                package_type = int(input('\nSelect Package type:\n1) PKG 300\n2) PKG 250\n3) PKG 230\n4) PKG 200\n5) Others..\n'))
                while package_type != 1 and package_type != 2 and package_type != 3 and package_type != 4 and package_type !=5:
                    package_type = int(input('\nINVALID PACKAGE!\nTry again..\nSelect Package type:\n1) PKG 300\n2) PKG 250\n3) PKG 230\n4) PKG 200\n5) Others..'))

                if package_type == 5:
                    package_type = input('\nEnter Package details\n')

                elif package_type == 1:
                    package_type = 'PKG 300'

                elif package_type == 2:
                    package_type = 'PKG 250'

                elif package_type == 3:
                    package_type = 'PKG 230'

                elif package_type == 4:
                    package_type = 'PKG 200'


                amt_paid = int(input('\nEnter the amount paid by the customer:\n'))
                while amt_paid > 9999:
                    amt_paid = int(input('\nINVALID AMOUNT!\nTry again..\nEnter the amount paid by the customer:\n'))

                remarks = False
                remarks_choice = int(input('\nAny remarks?\n1) Yes\n2) No\n'))
                if remarks_choice == 1:
                    remarks = input('\nEnter remarks below:\n')

                else:
                    print('\nData successfully captured!')


                start_program = LoadData(user_id, vc_num, receipt_num, package_type, amt_paid, remarks)                         
                writing_db = start_program.file_open()

                if writing_db == True:
                    print('\nSave Successful!')

                else:
                    print('\nERROR! FIle not saved!')

            else:
                print('\nVC data does not exist!\n')

        else:
            print('\nLogin failed!')


    elif login == 2:
        user_id = input('\nCreate a user name: ')
        user_id = user_id.encode()
        pwd = getpass('Create your password: ')
        pwd = pwd.encode()

        key_code = Keys
        code = key_code.read_key()

        key = Fernet(code)

        encrypted_pwd = key.encrypt(pwd)
        encrypted_id = key.encrypt(user_id)

        user_auth = Auth(encrypted_id, encrypted_pwd)

        login_status = user_auth.new_user()

        print(f'\n{login_status}')

    else:
        print('Invalid choice!')

if __name__ == "__main__":
    app.run(debug=True)




                                 

                                 


# In[ ]:




