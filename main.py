def readAndCheckData():
    import csv
    new_csv = []
    with open('telrecords.csv', 'r') as file:
        csv_file = csv.DictReader(file, delimiter=';')
        for i in csv_file:
            new_csv.append(i)
    while True:          
            target_phone = []
            caller_phone = []
            all_call = []
            phone = inputPhone()
            for row in new_csv:
                if row['caller']==phone:
                    caller_phone.append(row) # shu yerdan target telefonni topib olish mumkin
                elif row['recipient']==phone:
                    target_phone.append(row)  
                if row['caller'] == phone or row['recipient'] == phone:
                    all_call.append(row)   
            if len(caller_phone)>0 or len(target_phone)>0:
                return caller_phone, target_phone, all_call, phone
            else:
                print('Phone number not found!') 


def inputPhone():
    while True:
        phone = input('Enter your phone number: ')
        if len(phone)==12:
            return phone
        else:
            print('Please enter your number in the form below +79047886119')


def find_calls(calls):
    all_calls = len(calls)
    ac_calls, all_times, missed_calls, rejected_calls = 0,0,0,0

    for call in calls:
        if int(call['duration']) == -1:
            rejected_calls+=1
        elif int(call['duration']) == -2:
            missed_calls+=1
        else:
            all_times+=int(call['duration'])
            ac_calls+=1
    
    avarage_all_time = all_times/all_calls
    avarage_acc_time = all_times/ac_calls
    all_min = int(avarage_all_time/60)
    all_sec = int(avarage_all_time%60)
    acc_min = int(avarage_acc_time/60)
    acc_sec = int(avarage_acc_time%60)

    return all_calls, all_min, all_sec,ac_calls,acc_min,acc_sec,missed_calls,rejected_calls


def out_calls(calls):
    all_calls, all_min, all_sec,ac_calls,acc_min,acc_sec,missed_calls,rejected_calls = find_calls(calls)
    print('\n<<< Outgoing calls >>>\n')
    print(f'{all_calls} outgoing call(s), avarage time: {all_min} min {all_sec} sec')
    print(f'{ac_calls} accepted outgoing call(s), avarage time: {acc_min} min {acc_sec} sec')
    print(f'{missed_calls} missed outgoing call(s)')
    print(f'{rejected_calls} rejected outgoing call(s)')


def income_calls(calls):
    all_calls, all_min, all_sec,ac_calls,acc_min,acc_sec,missed_calls,rejected_calls = find_calls(calls)
    print('\n<<< Incoming calls >>>\n')
    print(f'{all_calls} incoming call(s), avarage time: {all_min} min {all_sec} sec')
    print(f'{ac_calls} accepted incoming call(s), avarage time: {acc_min} min {acc_sec} sec')
    print(f'{missed_calls} missed incoming call(s)')
    print(f'{rejected_calls} rejected incoming call(s)')


def inputOtherPhone(user_phone):
    while True:
        phone = input('Enter target phone number: ')
        if len(phone)==12:
            return phone
        elif phone == user_phone:
            print('Enter another number. This is your number!')
        else:
            print('Please enter target number in the form below +79047886119')


def find_target_phone(phone_list, user_phone):
    while True:
        target_list = []
        phone = inputOtherPhone(user_phone)
        for i in phone_list:
            if i['caller'] == user_phone and i['recipient'] == phone or i['caller'] == phone and i['recipient'] == user_phone:
                target_list.append(i)
        if len(target_list)>0:
            return target_list, phone
        print('Phone number not found in the database!')


def writer(target_list,user_phone, target_phone):
    with open(f'{user_phone}\_{target_phone}.txt', 'w') as file:
        write_text = struc_text(target_list,user_phone)
        for i in write_text:
            file.write(i+'\n')


def struc_text(target_list,phone_num):
    for phone in target_list:
        if phone['caller'] == phone_num:
            if int(phone['duration']) ==-1:
                call_times = 'rejected'
            elif int(phone['duration']) ==-2:
                call_times = 'missed'
            else:
                time = int(phone['duration'])
                call_times = f'{int(time/60)} min {int(time%60)} sec'
            date = phone['dt']
            text = f'Out: {date} - {call_times}'
        elif phone['recipient'] == phone_num:
            if int(phone['duration']) ==-1:
                call_times = 'rejected'
            elif int(phone['duration']) ==-2:
                call_times = 'missed'
            else:
                time = int(phone['duration'])
                call_times = f'{int(time/60)} min {int(time%60)} sec'
            date = phone['dt']
            text = f'In: {date} - {call_times}'
        yield text


def target_phone(all_call, phone_num):
    from datetime import datetime
    target_list, phone_other = find_target_phone(all_call, phone_num)
    target_list = sorted(target_list,key=lambda date: datetime.strptime(date['dt'], "%Y-%m-%d %H:%M:%S"), reverse=True)
    text = struc_text(target_list, phone_num)
    for i in text:
        print(i)
    writer(target_list,phone_num, phone_other)
    print(f'Call history saved in file {phone_num}\_{phone_other}.txt')


def option():
    print('\nSelect an action:\n1 - Call statistics\n2 - Call history with other contact\n3 - Exit')
    while True:
        try:
            value = int(input('Your choice: '))
            if value == 1:
                return 1
            elif value == 2:
                return 2
            elif value == 3:
                return 3
            else:
                print('Please select a section in the menu!')
        except:
            print('Please select a section in the menu!')


def dashboard():
    out_phone,in_phone,all_call, phone_num = readAndCheckData()
    while True:
        value = option()
        if value == 1:
            out_calls(out_phone)
            income_calls(in_phone)
        elif value ==2:
            target_phone(all_call, phone_num)
        else:
            dashboard()


dashboard()