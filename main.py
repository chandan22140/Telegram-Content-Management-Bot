import os


import telebot
import random
import datetime as dt
import math
import keep_alive
import json
import traceback
os.environ['API_KEY'] = "API_KEY"

API_KEY = os.environ['API_KEY']

bot = telebot.TeleBot(API_KEY, parse_mode=None)
buttonnn = telebot.types.KeyboardButton
keyboard = telebot.types.ReplyKeyboardMarkup

affiliates = [
    "Have you got any feedback?  Do send them to @chandanwaaa"
]

greetings = ["hi", "hello", "wassup", "what's up", "namaste"]


# user_data = {
#               800851598:{"firstName":"Chandan" , 
#                         "lastName": "Sah" ,
#                         "username":800851598}}
f = open("user_data.json")
user_data = json.load(f)
f.close()
# current_institute = user_data[str(message.chat.id)]["current_institute"]
# current_year = user_data[str(message.chat.id)]["current_year"]
# current_block = user_data[str(message.chat.id)]["current_block"]
# current_course = user_data[str(message.chat.id)]["current_course"]
# current_content_type = user_data[str(message.chat.id)]["current_content_type"]



# institute_architecture_json = {
#     
#     "IIITD": {
#         "1": {
#             "SEM_2": {
#                 "CSE":{
#                     "DSA": "IIITD_DSA_CSE102"
#                 }
#             }
#         }
#     }
# }

# course_content_json = {
#         "IIITD_DSA_CSE102":{
#                 "PYQS":[]
#         }
#     }
architect_json = {
    "IIITD":[ 5728953096, 1172086482, 800851598]
}
chandan_list = [800851598, 1174104456]

upload_requests_json = {}
# if restarting the server then set request_count to appropriate (bigger) number
request_count = 0


f = open("upload_requests.json")
upload_requests_json = json.load(f)
f.close()


f = open("institute_architecture.json")
institute_architecture_json = json.load(f)
f.close()

f = open("course_content.json")
course_content_json = json.load(f)
f.close()

import csv 

f = open("data.csv", "r") 
list_of_list = []
csv_r = csv.reader(f, delimiter=',')
accronym2course_hash = {}

for row in csv_r:

    list_of_list.append(row)
    year = row[0].upper()
    block = row[1].upper()
    dept =  row[2].upper()
    accronym =  row[3].upper()
    code =  row[4].upper()
    course_hash = "IIITD_"+row[3]+"_"+row[4]
    if "IIITD" not in institute_architecture_json.keys():
        institute_architecture_json["IIITD"]={}
    if year not in institute_architecture_json["IIITD"].keys():
        institute_architecture_json["IIITD"][year]={}
    
    if block not in institute_architecture_json["IIITD"][year].keys():
        institute_architecture_json["IIITD"][year][block]={}
    
    if dept not in institute_architecture_json["IIITD"][year][block].keys():
        institute_architecture_json["IIITD"][year][block][dept]={}
    
    if accronym not in institute_architecture_json["IIITD"].keys():
        institute_architecture_json["IIITD"][year][block][dept][accronym]=course_hash

    if accronym not in accronym2course_hash:
        accronym2course_hash[accronym] = course_hash

    if course_hash not in course_content_json:
        course_content_json[course_hash]={}


f.close()

out_file = open("accronym2course_hash.json", "w")
json.dump(accronym2course_hash, out_file, indent = 4)
out_file.close()

out_file = open("institute_architecture.json", "w")
json.dump(institute_architecture_json, out_file, indent = 4)
out_file.close()

out_file = open("course_content.json", "w")
json.dump(course_content_json, out_file, indent = 4)
out_file.close()


def validgreetings(message):
    return message.text.lower() in greetings

def valid_inst_Req(message):
    query = message.text
    if (query.upper() in institute_architecture_json.keys()):
        return True
    else:
        return False


valid_marketer_code = "6276305367861AAFUiGkkuRGlRMlM4ipcSKq1zvQYZsU"
def valid_marketer(message):
    return (message.text == valid_marketer_code)



valid_uploader_code = "627623430klhjgfdsfgchjk5361AAFUihhhhGfgfhgjuRGlRMIR0tSKq1zYZsU"
def valid_uploader(message):
    return (message.text == valid_uploader_code)

valid_architect_code = "6276234305361AAFkjhgfUihhhhGfgfhgjuRGlRMIR0tSKq1zYZsU"
def valid_architect(message):
    return (message.text == valid_architect_code)

def sized_custom_keypad(lis):
    toret = keyboard(resize_keyboard=True, one_time_keyboard=True)
    l = len(lis)
    num_of_rows = math.ceil(l/3) 
    for i in range(num_of_rows):
        if (i!=(num_of_rows-1)):
            toret.add(buttonnn(lis[3*i]),buttonnn(lis[3*i+1]),buttonnn(lis[3*i+2]))
        else:
            # remaining_button_count==val
            val = (l-(num_of_rows-1)*3)
            # print(val)
            if(val==1):
                toret.add(buttonnn(lis[3*i]))
            if(val==2):
                toret.add(buttonnn(lis[3*i]), buttonnn(lis[3*i+1]))
            if(val==3):
                toret.add(buttonnn(lis[3*i]), buttonnn(lis[3*i+1]), buttonnn(lis[3*i+2]))
            return toret

def get_institute_options():

    lis = sorted(list(institute_architecture_json.keys()))
    return sized_custom_keypad(lis=lis)

def get_year_options(message):
    global user_data
    current_institute = user_data[str(message.chat.id)]["current_institute"]
    
    lis = sorted(list(institute_architecture_json[current_institute].keys()))

    return sized_custom_keypad(lis=lis)

def get_block_options(message):
    global user_data
    current_institute = user_data[str(message.chat.id)]["current_institute"]
    current_year = user_data[str(message.chat.id)]["current_year"]

    lis = sorted(list(institute_architecture_json[current_institute][current_year].keys()))

    return sized_custom_keypad(lis=lis)

def get_department_options(message):
    global user_data
    current_institute = user_data[str(message.chat.id)]["current_institute"]
    current_year = user_data[str(message.chat.id)]["current_year"]
    current_block = user_data[str(message.chat.id)]["current_block"]

    lis = sorted(list(institute_architecture_json[current_institute][current_year][current_block].keys()))

    return sized_custom_keypad(lis=lis)

def get_courses_options(message):
    global user_data
    current_institute = user_data[str(message.chat.id)]["current_institute"]
    current_year = user_data[str(message.chat.id)]["current_year"]
    current_block = user_data[str(message.chat.id)]["current_block"]
    current_department = user_data[str(message.chat.id)]["current_department"]

    lis = sorted(list(institute_architecture_json[current_institute][current_year][current_block][current_department].keys()))

    return sized_custom_keypad(lis=lis)

def get_content_type_options(message):
    global user_data
    current_institute = user_data[str(message.chat.id)]["current_institute"]
    current_year = user_data[str(message.chat.id)]["current_year"]
    current_block = user_data[str(message.chat.id)]["current_block"]
    current_department = user_data[str(message.chat.id)]["current_department"]
    current_course = user_data[str(message.chat.id)]["current_course"]

    current_course_hash = institute_architecture_json[current_institute][current_year][current_block][current_department][current_course]
    user_data[str(message.chat.id)]["current_course_hash"] = current_course_hash
    lis = sorted(list(course_content_json[current_course_hash].keys()))+["DONE"]

    # toret = keyboard(row_width=2, resize_keyboard=True, one_time_keyboard=True)

    return sized_custom_keypad(lis=lis)


def get_mode_options(message):
    global user_data
    current_course = user_data[str(message.chat.id)]["current_course"]
    current_content_type = user_data[str(message.chat.id)]["current_content_type"] 
    current_course_hash = user_data[str(message.chat.id)]["current_course_hash"] 
    

    toret = keyboard(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    option1 = f'Upload new file for {current_content_type} of {current_course}'
    lis = [option1]

    if current_content_type in list(course_content_json[current_course_hash].keys()):
        option2 = f'Download existing {current_content_type}'
        lis.append(option2)

    for i in lis:
        toret.add(buttonnn(i))
    return toret

def get_request_response():
    toret = keyboard(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    option1 = f'Reject Completely(0)'
    option2 = f'Upload after mannual edit(0.5)'
    option3 = f'Accept Completely and Upload(1)'
    
    lis = [option1, option2, option3]
    for i in lis:
        toret.add(buttonnn(i))
    return toret



def unix_to_ist(unix_number):
    utc_datetime = dt.datetime.utcfromtimestamp(unix_number)

    ist_timezone = dt.timezone(dt.timedelta(hours=5, minutes=30))
    ist_datetime = utc_datetime.replace(tzinfo=dt.timezone.utc).astimezone(ist_timezone)

    ist_time_str = ist_datetime.strftime('%Y-%m-%d %H:%M:%S')

    return ist_time_str

def ist_now():
    utc_datetime = dt.datetime.utcnow()
    ist_timezone = dt.timezone(dt.timedelta(hours=5, minutes=30))
    ist_datetime = utc_datetime.replace(tzinfo=dt.timezone.utc).astimezone(ist_timezone)

    ist_time_str = ist_datetime.strftime('%Y-%m-%d %H:%M:%S')

    return ist_time_str




#........................ basic/profile section starts ............................................................

valid_content_type = ["END_SEM","MID_SEM","QUIZ", "PRACTICE_QUESTION" , "BOOK", "NOTES_SYLLABUS", "LECTURE_SLIDES", "LAB" , "PLAYLISTS", "ASSIGNMENTS"]


@bot.message_handler(commands=['ask_help'])
def ask_help(message):
    msg = bot.send_message(
        chat_id=message.chat.id, text="Please watch our tutorial on how to use our bot in best way\nhttps://www.youtube.com/watch?v=AuO9q0sPXV8\nYou can also contact @chandanwaaa for further help!"
        , reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['feedback'])
def ask_feedback(message):
    msg = bot.send_message(
        chat_id=message.chat.id, text="You may also contact Chnadan Sah ( @chandanwaaa ) for any feedback/suggestion or complaint!"
        , reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['edit_profile'])
def edit_profile(message):
    msg = bot.send_message(
        chat_id=message.chat.id, text="(EDIT_PROFILE MODE) Re-enter your Institute, Year, Semester one after another."
       )
    user_data[str(message.chat.id)]["is_complte"]==0
    ask_institute(message)

@bot.message_handler(commands=['start', 'restart'])
def send_welcome(message):
    # global current_institute
    bot.send_message(
        chat_id=message.chat.id, text="Hi " + message.from_user.first_name +
        "! \nI am Fuddu. :)\nI am still working on myself to get better. Currently I can provide you some helpful past papers/notes from some institutions & academic levels.\n\n")
    # ask_institute(message)
    try:
        if user_data[str(message.chat.id)]["is_complte"]==0:
            # ask to complete
            bot.send_message(chat_id=message.chat.id, text="Your profile is incomplete. Re-enter your Institute, Year, Semester one after another.")
            ask_institute(message)
        else:
            ask_department(message)

    except:
        user_data[str(message.chat.id)] = {
                        "is_complte":0,  
                        "firstName":message.chat.first_name , 
                        "lastName":message.chat.last_name ,
                        "username":message.chat.username,
                        "current_institute":"",
                        "current_year":"",
                        "current_block":"",
                        "current_department":"",
                        "current_content_type":"",
                        "current_course":"",
                        "current_course_hash":"",
                        "current_file_id":"",
                        "current_file_description":""
                        }


      # ask to complete
        bot.send_message(chat_id=message.chat.id, text="We are creating your new profile. \nEnter your Institute, Year, Semester one after another.")
        ask_institute(message)

def ask_institute(message):
    institute_options = get_institute_options()
    msg = bot.send_message(
        chat_id=message.chat.id, text="🏫Choose your Institute:\nYou may also: \n/restart\n/ask_help \n/edit_profile "
        , reply_markup=institute_options)
    bot.register_next_step_handler(msg, ask_year)

def ask_year(message):
    global user_data
    try: 
        if(message.text[0] == "/"):
            command_redirector(message)
            
        elif(message.text == "/ask_help"):
            ask_help(message)
            
        else:
            user_data[str(message.chat.id)]["current_institute"] = message.text.upper()
            year_options = get_year_options(message)
            msg= bot.send_message(chat_id=message.chat.id,text= "🎓Choose your Year:\nYou may also: \n/restart\n/ask_help \n/edit_profile ", reply_markup=year_options)
            bot.register_next_step_handler(msg, ask_block )

    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(message.chat.id,"Looks like you gave wrong input :P\n ")
        ask_institute(message)


def ask_block(msg_year_num):
    global user_data
    try: 
        if(msg_year_num.text[0] == "/"):
            command_redirector(msg_year_num)
        elif(msg_year_num.text == "/ask_help"):
            ask_help(msg_year_num)
        else:
            user_data[str(msg_year_num.chat.id)]["current_year"] = msg_year_num.text.upper()
            
            block_options = get_block_options(msg_year_num)
            msg = bot.send_message(chat_id=msg_year_num.chat.id, text="🗓️Choose your Semester/Block/System:\nYou may also: \n/restart\n/ask_help \n/edit_profile ", reply_markup=block_options)
            bot.register_next_step_handler(msg, profile_complete)

    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(msg_year_num.chat.id,"Looks like you gave wrong input :P\n ")
        ask_year(msg_year_num)

def profile_complete(msg_block_name):
    global user_data
    try: 
        if(msg_block_name.text[0] == "/"):
            command_redirector(msg_block_name)
        elif(msg_block_name.text == "/ask_help"):
            ask_help(msg_block_name)
        else:
            user_data[str(msg_block_name.chat.id)]["current_block"] = msg_block_name.text.upper()
            # set is_complte 1, once completed
            user_data[str(msg_block_name.chat.id)]["is_complte"] = 1

            f = open("user_data.json", "w")
            json.dump(user_data,f, indent =4)
            f.close()            

            bot.send_message(msg_block_name.chat.id,"Your profile is complete :)\n ")
            ask_department(msg_block_name)
    except Exception:
        bot.send_message(msg_block_name.chat.id,"Looks like you gave wrong input :P\n ")
        ask_block(msg_block_name)  



def ask_department(msg):
    try: 
        department_options = get_department_options(msg)
        msg = bot.send_message(chat_id=msg.chat.id, text="🏬Choose the department which offers the course you need help(resources) with:\nYou may also: \n/restart\n/ask_help \n/edit_profile ", reply_markup=department_options)
        bot.register_next_step_handler(msg, ask_course)

    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(msg.chat.id,"Looks like you gave wrong input :P\n ")
        ask_year(msg)
        
def ask_course(msg_department_name):
    global user_data
    try: 
        if(msg_department_name.text[0] == "/"):
            command_redirector(msg_department_name)
        elif(msg_department_name.text == "/ask_help"):
            ask_help(msg_department_name)
        else:        
            user_data[str(msg_department_name.chat.id)]["current_department"] = msg_department_name.text.upper()
            course_options = get_courses_options(msg_department_name)
            msg = bot.send_message(chat_id=msg_department_name.chat.id,text= "📖Choose Course you need help(resources) with:\nYou may also: \n/restart\n/ask_help\n", reply_markup=course_options)
            bot.register_next_step_handler(msg, ask_content_type)

    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(msg_department_name.chat.id,"Looks like you gave wrong input :P\n ")
        ask_block(msg_department_name)

def ask_content_type (msg_course_name):
    try:
        if(msg_course_name.text[0] == "/"):
            command_redirector(msg_course_name)
        elif(msg_course_name.text == "/ask_help"):
            ask_help(msg_course_name)
        else:        
            user_data[str(msg_course_name.chat.id)]["current_course"] = msg_course_name.text.upper()
            content_type_options = get_content_type_options(msg_course_name)
            msg = bot.send_message(chat_id=msg_course_name.chat.id,text= f"📋Choose content_type:\n\nFor Uploading, Suggested content_types for uploading are:\n {valid_content_type} \nYou may also: \n/restart\n/ask_help \n/edit_profile \n", reply_markup=content_type_options)
            bot.register_next_step_handler(msg, ask_mode)

    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(msg_course_name.chat.id,"Looks like you gave wrong input :P\n ")
        ask_course(msg_course_name)

def ask_mode (msg_content_type):
    try:
        if(msg_content_type.text[0] == "/"):
            command_redirector(msg_content_type)
        elif(msg_content_type.text == "/ask_help"):
            ask_help(msg_content_type)
        elif(msg_content_type.text == "DONE"):
            bot.send_message(msg_content_type.chat.id, f"Thank you using out bot!\n\n"+affiliates[random.randint(0, len(affiliates)-1)], reply_markup=telebot.types.ReplyKeyboardRemove())
        else:
            # if msg_content_type.text.upper()  in valid_content_type:
            user_data[str(msg_content_type.chat.id)]["current_content_type"] = msg_content_type.text.upper()
            mode_options = get_mode_options(msg_content_type)
            msg = bot.send_message(chat_id=msg_content_type.chat.id,text= "Choose mode:\nYou may also: \n/restart\n/ask_help \n/edit_profile \n", reply_markup=mode_options)

            bot.register_next_step_handler(msg, redirect_user)
                # print(user_data[str(msg_content_type.chat.id)]["current_content_type"])
            # else:
            #     msg = bot.send_message(chat_id=msg_content_type.chat.id,text= f"Invalid content_type. \n📋Choose content_type:\nFor Uploading, Currently available content_type are:\n {valid_content_type}",  reply_markup=get_content_type_options(msg_content_type))
            #     bot.register_next_step_handler(msg, ask_mode)

            

    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(msg_content_type.chat.id,"Looks like you gave wrong input :P\n ")
        ask_course(msg_content_type)

def redirect_user(msg_mode_type):
    try:
        if(msg_mode_type.text[0] == "/"):
            command_redirector(msg_mode_type)
        elif(msg_mode_type.text == "/ask_help"):
            ask_help(msg_mode_type)
        else:
            current_course = user_data[str(msg_mode_type.chat.id)]["current_course"]
            current_content_type = user_data[str(msg_mode_type.chat.id)]["current_content_type"] 
            option_upload = f'Upload new file for {current_content_type} of {current_course}'
            option_download =  f'Download existing {current_content_type}'
            if(msg_mode_type.text == option_download):
                send_content(msg_mode_type) 
            elif(msg_mode_type.text == option_upload):
                ask_for_file__up(msg_mode_type)
            else:
                bot.send_message(msg_mode_type.chat.id,"Looks like you gave wrong input :P\n ")
                ask_mode(msg_mode_type)


    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(msg_mode_type.chat.id,"Looks like you gave wrong input :P\n ")
        ask_mode(msg_mode_type)


def send_content (msg_mode_type):
    try:
        if(msg_mode_type.text[0] == "/"):
            command_redirector(msg_mode_type)
        elif(msg_mode_type.text == "/ask_help"):
            ask_help(msg_mode_type)
        else:
            global user_data

            current_institute = user_data[str(msg_mode_type.chat.id)]["current_institute"]
            current_year = user_data[str(msg_mode_type.chat.id)]["current_year"]
            current_block = user_data[str(msg_mode_type.chat.id)]["current_block"]
            current_department = user_data[str(msg_mode_type.chat.id)]["current_department"]
            current_course = user_data[str(msg_mode_type.chat.id)]["current_course"]
            current_course_hash = institute_architecture_json[current_institute][current_year][current_block][current_department][current_course]
            current_content_type  = user_data[str(msg_mode_type.chat.id)]["current_content_type"]


            bot.send_message(msg_mode_type.chat.id, f"Fetching {current_course}'s {current_content_type} ...")

            for ele_index in range(len(course_content_json[current_course_hash][current_content_type])):
                file_id = course_content_json[current_course_hash][current_content_type][ele_index][0]
                file_description = course_content_json[current_course_hash][current_content_type][ele_index][1]
                bot.send_document(chat_id = msg_mode_type.chat.id, caption=f'({ele_index+1}) {file_description}', document=file_id )
            # log_content_start
            print()
            print(ist_now())
            print(str(msg_mode_type.chat.id)+" downloaded following:")
            print(user_data[str(msg_mode_type.chat.id)])
            # log_content_end
            print()

            content_type_options = get_content_type_options(msg_mode_type)
            msg = bot.send_message(msg_mode_type.chat.id, f"Choose another content_type \nFor Uploading, Suggested content_type are:\n {valid_content_type} or press last option(DONE):\nYou may also: \n/restart\n/ask_help\n", reply_markup=content_type_options)
            # ask another content_type 
            bot.register_next_step_handler(msg, ask_mode)

    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(msg_mode_type.chat.id,"Looks like you gave wrong input :P\n ")
        ask_institute(msg_mode_type)

#........................ user_query section ends ............................................................

#........................ uploader_admin section starts ............................................................


def send_request(architect_id_int, architect_username, user_message):

    current_file_description=user_data[str(user_message.chat.id)]["current_file_description"]
    current_file_id = user_data[str(user_message.chat.id)]["current_file_id"]
    
    msg = bot.send_document(chat_id=architect_id_int,document=current_file_id ,caption=current_file_description, reply_markup= get_request_response())
    print(msg.date)
    
    upload_requests_json[str(architect_id_int)+":"+str(msg.message_id)] = {
        "architect_id":architect_id_int,
        "architect_username":architect_username,        
        "uploader_id":user_message.chat.id,
        "current_institute":user_data[str(user_message.chat.id)]["current_institute"],
        "current_year":user_data[str(user_message.chat.id)]["current_year"],
        "current_block":user_data[str(user_message.chat.id)]["current_block"],
        "current_department":user_data[str(user_message.chat.id)]["current_department"],
        "current_course":user_data[str(user_message.chat.id)]["current_course"],
        "current_course_hash":user_data[str(user_message.chat.id)]["current_course_hash"],
        "current_content_type":user_data[str(user_message.chat.id)]["current_content_type"],
        "current_file_id":current_file_id,
        "current_file_description": current_file_description
        }
    f = open("upload_requests.json", "w")
    json.dump(upload_requests_json,f, indent =4)
    f.close()  

    bot.register_for_reply(msg, send_response_2_uploader)


def send_response_2_uploader(architect_response):
    bot_ka_request_message = architect_response.reply_to_message
    unix_time_of_upload = bot_ka_request_message.date

    request_id = str(architect_response.chat.id)+":"+str(bot_ka_request_message.message_id)
    # this request_id is unique for this bot
    uploader_id  = upload_requests_json[request_id]["uploader_id"]

    if (architect_response.text=='Reject Completely(0)'):
       bot.send_message(
        chat_id=uploader_id, text=f"Your upload at {unix_to_ist(unix_time_of_upload)} was Rejected)")
    else:
        user_data[str(architect_response.chat.id)]["current_institute"] = upload_requests_json[request_id]["current_institute"]
        user_data[str(architect_response.chat.id)]["current_year"] = upload_requests_json[request_id]["current_year"]
        user_data[str(architect_response.chat.id)]["current_block"] = upload_requests_json[request_id]["current_block"]
        user_data[str(architect_response.chat.id)]["current_department"] = upload_requests_json[request_id]["current_department"]
        user_data[str(architect_response.chat.id)]["current_course"] = upload_requests_json[request_id]["current_course"]
        user_data[str(architect_response.chat.id)]["current_course_hash"] = upload_requests_json[request_id]["current_course_hash"]
        user_data[str(architect_response.chat.id)]["current_content_type"] = upload_requests_json[request_id]["current_content_type"]
        user_data[str(architect_response.chat.id)]["current_file_id"] = upload_requests_json[request_id]["current_file_id"]
        user_data[str(architect_response.chat.id)]["current_file_description"] = upload_requests_json[request_id]["current_file_description"]
       
        to_be_uploaded_course_hash= user_data[str(architect_response.chat.id)]["current_course_hash"]
        to_be_uploaded_content_type = user_data[str(architect_response.chat.id)]["current_content_type"]
        to_be_uploaded_file_id = user_data[str(architect_response.chat.id)]["current_file_id"] 
        to_be_uploaded_file_description = user_data[str(architect_response.chat.id)]["current_file_description"]
        
        if(architect_response.text=='Accept Completely and Upload(1)'):
            bot.send_message(
            chat_id=uploader_id, text=f"Your upload at {unix_to_ist(unix_time_of_upload)} was Accepted Completely")
            course_content_json[to_be_uploaded_course_hash][to_be_uploaded_content_type].append([to_be_uploaded_file_id, to_be_uploaded_file_description])

        
        elif(architect_response.text=='Upload after mannual edit(0.5)'):
            bot.send_message(
            chat_id=uploader_id, text=f"Your upload at {unix_to_ist(unix_time_of_upload)} was Accepted partially and will be uploaded after mannual edit")

            ask_for_file__up(architect_response)

        # log_content_start
        print()
        print(ist_now())
        print(str(architect_response.chat.id)+" uploaded_content as following:")
        print()
        # log_content_end
        
        upload_requests_json.pop(request_id)

        f = open("upload_requests.json", "w")
        json.dump(upload_requests_json,f, indent =4)
        f.close()          



def ask_for_file__up(msg_mode_type):
# ask for file
    try: 
        if(msg_mode_type.text[0] == "/"):
            command_redirector(msg_mode_type)   

        msg = bot.send_message(msg_mode_type.chat.id, "(ADMIN MODE)Send file to be stored \n(enter PDFs only if you have set of images merge them to pdf, \nOr enter DONE\nYou may also: \n/restart\n/ask_help \n/edit_profile \n")
        bot.register_next_step_handler(msg, generate_fileid_and_redirect__up)
        # print(user_data[str(msg_mode_type.chat.id)])
            
    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        
        bot.send_message(
            msg_mode_type.chat.id,
            "Looks like you gave wrong input :P\nSend /help to know what I understand.\n Starting over again\n"
            )

# Send another file or DONE or send another content_type or send new course hash or ")

def generate_fileid_and_redirect__up(msg_file: telebot.types.Message):
    try: 
        global user_data

        to_be_uploaded_institute = user_data[str(msg_file.chat.id)]["current_institute"]     
        to_be_uploaded_year = user_data[str(msg_file.chat.id)]["current_year"]     
        to_be_uploaded_block = user_data[str(msg_file.chat.id)]["current_block"]     
        to_be_uploaded_department = user_data[str(msg_file.chat.id)]["current_department"]

        to_be_uploaded_course= user_data[str(msg_file.chat.id)]["current_course"]
        to_be_uploaded_course_hash= user_data[str(msg_file.chat.id)]["current_course_hash"]
        to_be_uploaded_content_type = user_data[str(msg_file.chat.id)]["current_content_type"]

        # global valid_content_type
        # global course_content_json
                
        if((msg_file.text)and(msg_file.text[0] == "/")):
            command_redirector(msg_file)

        elif((msg_file.text)and(msg_file.text.upper()== "DONE" )):
            # autosave / DONE 
            resave_course_content(msg_file)    
            msg = bot.send_message(msg_file.chat.id, f'Successfully exited Admin mode ')

        elif((msg_file.text)and(msg_file.text.upper() in valid_content_type )):
            # if sent another content_type 
            user_data[str(msg_file.chat.id)]["current_content_type"] = msg_file.text.upper()
            # then ask for files
            msg = bot.send_message(msg_file.chat.id, f'(ADMIN MODE) Send new files to upload under content_type: {msg_file.text.upper()}  \nof course: {to_be_uploaded_course}')
            bot.register_next_step_handler(msg, generate_fileid_and_redirect__up)

        elif((msg_file.document)and(msg_file.document.file_id)):
            # sent (another) file
            # print(msg_file.caption)
            # print(type(msg_file.caption))
            if (msg_file.caption==None):
                msg = bot.send_message(msg_file.chat.id, 'You can\'t upload without pasting description/name in the caption section. ')
                bot.register_next_step_handler(msg, generate_fileid_and_redirect__up)
                return 0
            
            if ((msg_file.document.file_name.split("."))[-1].lower()!="pdf"):
                msg = bot.send_message(msg_file.chat.id, 'Only PDFs can be uploaded. You can\'t upload other filetypes. ')
                bot.register_next_step_handler(msg, generate_fileid_and_redirect__up)
                return 0
            
            to_be_uploaded_caption = msg_file.caption
            file__id = msg_file.document.file_id
            user_data[str(msg_file.chat.id)]["current_file_id"] = file__id
            user_data[str(msg_file.chat.id)]["current_file_description"] = to_be_uploaded_caption

            # checking 
            if to_be_uploaded_content_type not in course_content_json[to_be_uploaded_course_hash]:
                course_content_json[to_be_uploaded_course_hash][to_be_uploaded_content_type]=[]

            if to_be_uploaded_course_hash not in upload_requests_json:
                upload_requests_json[to_be_uploaded_course_hash]={}

            if to_be_uploaded_content_type not in upload_requests_json[to_be_uploaded_course_hash]:
                upload_requests_json[to_be_uploaded_course_hash][to_be_uploaded_content_type]=[]

            # checking if its a valid institute architect
            # print(architect_json[to_be_uploaded_institute]+chandan_list)
            if msg_file.chat.id  in (architect_json[to_be_uploaded_institute]+chandan_list):
                # its a valid institute architect
                course_content_json[to_be_uploaded_course_hash][to_be_uploaded_content_type].append([file__id, to_be_uploaded_caption])

                # log_content_start
                print()
                print(ist_now())
                print(str(msg_file.chat.id)+" uploaded_content as following:")
                print(user_data[str(msg_file.chat.id)])
                # log_content_end
                print()
                
            else:
                # not a valid institute architect
                # create a request to one of the valid institute architect
                print(to_be_uploaded_institute)
                num_architects = len(architect_json[to_be_uploaded_institute])
                print(num_architects)

                idx = random.randint(0,num_architects-1)
                print(idx)

                id = architect_json[to_be_uploaded_institute][idx]

                
                username = user_data[str(id)]["username"]
                name = user_data[str(id)]["firstName"]+" "+user_data[str(id)]["lastName"]
                send_request(id,username,  msg_file)
                bot.send_message(chat_id=msg_file.chat.id, text=f"Your upload request is sent to {to_be_uploaded_institute}'s acrchitect:\n{name} \n@{username}\nYou will be informeded once they approve or deny")
            
            msg = bot.send_message(chat_id=msg_file.chat.id, text=f"(ADMIN MODE)\n\nSend: \nDONE to stop and exit the ADMIN MODE. \nOR\n\nSend another file to upload under content_type: {to_be_uploaded_content_type}  \nof course: {to_be_uploaded_course}') \nOR\n\nSend another content_type under course: {to_be_uploaded_course} where you wish to upload the file\nFor Uploading, Suggeste content_type are:\n {valid_content_type}\nOR\n\nSend an existing course name under current department: {to_be_uploaded_department}")
            bot.register_next_step_handler(msg, generate_fileid_and_redirect__up)
        elif(msg_file.text):
            # sent  course name
            
            # if text is valid course name given a 
            if msg_file.text.upper() in institute_architecture_json[to_be_uploaded_institute][to_be_uploaded_year][to_be_uploaded_block][to_be_uploaded_department].keys():
                to_be_uploaded_course = msg_file.text.upper()
                to_be_uploaded_course_hash = institute_architecture_json[to_be_uploaded_institute][to_be_uploaded_year][to_be_uploaded_block][to_be_uploaded_department][to_be_uploaded_course]
                
                ask_content_type(msg_file)
            else:
                msg = bot.send_message(chat_id=msg_file.chat.id, text=f"This course name should be alreadly existing under current department (the department that u last chose). \n To create a new course name enter Architect mode using the code, and create course there.\n Send an existing course name under current department you chose.")
                bot.register_next_step_handler(msg, generate_fileid_and_redirect__up)

    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(
            msg_file.chat.id,
            "Looks like you gave wrong input(may be a text instead of file) :P\nSend /help to know what I understand.\n Starting over again\n"
            )


#........................ uploader section finish ............................................................

#........................ architect section starts ............................................................

@bot.message_handler(func=valid_architect)
def ask_institute__up(message):
    try: 
        global user_data 
        if  (message.chat.id in chandan_list)or (message.chat.id in architect_json[message.text.upper()]):
            msg = bot.send_message(message.chat.id, "(ARCHITECT MODE)Send Institute name corresponding to file to be stored, ")
            bot.register_next_step_handler(msg, ask_year_num__up)
        else:
            bot.send_message(message.chat.id, "Unauthorized. You are not an architect of this institute.")
            return 0
    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(
            message.chat.id,
            "Looks like you gave wrong input :P\nSend /help to know what I understand.\n Starting over again\n"
            )

def ask_year_num__up(institute_name_msg):
    try: 
        global user_data 
        user_data[str(institute_name_msg.chat.id)]["current_institute"] = institute_name_msg.text.upper()
        msg = bot.send_message(institute_name_msg.chat.id, "(ARCHITECT MODE)Send Year number corresponding to file to be stored\nEnter /escape if you want to escape from this mode.\n")
        bot.register_next_step_handler(msg, ask_block__up)

    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(
            institute_name_msg.chat.id,
            "Looks like you gave wrong input :P\nSend /help to know what I understand.\n Starting over again\n"
            )

def ask_block__up(msg_year_num):
    try: 
        if(escape_function(msg_year_num)==1):
            return 0
        elif(escape_function(msg_year_num)==2):
            ask_help(msg_year_num)

        global user_data 
        user_data[str(msg_year_num.chat.id)]["current_year"] = msg_year_num.text.upper()
        msg = bot.send_message(msg_year_num.chat.id, "(ARCHITECT MODE)Send Block name corresponding to file to be stored, \nEnter /escape if you want to escape from this mode.\n")

        bot.register_next_step_handler(msg, ask_dept__up)

    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(
            msg_year_num.chat.id,
            "Looks like you gave wrong input :P\nSend /help to know what I understand.\n Starting over again\n"
            )

def ask_dept__up(msg_block_name):
    try: 
        if(escape_function(msg_block_name)==1):
            return 0
        elif(escape_function(msg_block_name)==2):
            ask_help(msg_block_name)  
                   
        global user_data 
        user_data[str(msg_block_name.chat.id)]["current_block"] = msg_block_name.text.upper()
        msg = bot.send_message(msg_block_name.chat.id, "(ARCHITECT MODE)Send Department name of course/file that you are uploading \nEnter /escape if you want to escape from this mode.\n")
        bot.register_next_step_handler(msg, ask_course_name__up)

    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(
            msg_block_name.chat.id,
            "Looks like you gave wrong input :P\nSend /help to know what I understand.\n Starting over again\n"
            )
        
def ask_course_name__up(msg_department_name):
    try: 
        if(escape_function(msg_department_name)==1):
            return 0
        elif(escape_function(msg_department_name)==2):
            ask_help(msg_department_name)   
                   
        if(msg_department_name.text.upper()=='DONE'):
            msg = bot.send_message(msg_department_name.chat.id, "Architect mode exited successfully, and changes saved.")
            # autosave
            resave_institute_architecture(msg_department_name)    
            resave_course_content(msg_department_name)   
        else:    
            global user_data
            user_data[str(msg_department_name.chat.id)]["current_department"] = msg_department_name.text.upper()
            msg = bot.send_message(msg_department_name.chat.id, "(ARCHITECT MODE) Send Course name corresponding to that department \nEnter /escape if you want to escape from this mode.\n")
            bot.register_next_step_handler(msg, ask_course_hash_name__up)

    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(
            msg_department_name.chat.id,
            "Looks like you gave wrong input :P\nSend /help to know what I understand.\n Starting over again\n"
            )


def ask_course_hash_name__up(msg_course_name):
    try: 
        if(escape_function(msg_course_name)==1):
            return 0
        elif(escape_function(msg_course_name)==2):
            ask_help(msg_course_name)
                   
        global user_data
        user_data[str(msg_course_name.chat.id)]["current_course"] = msg_course_name.text.upper()
        msg = bot.send_message(msg_course_name.chat.id, "(ARCHITECT MODE) Send Course hash name corresponding to file to be stored, \nEnter /escape if you want to escape from this mode.\n")
        bot.register_next_step_handler(msg, redirector_architect)

    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        bot.send_message(
            msg_course_name.chat.id,
            "Looks like you gave wrong input :P\nSend /help to know what I understand.\n Starting over again\n"
            )

def redirector_architect(msg_course_hash_name):
    try: 
        if(escape_function(msg_course_hash_name)==1):
            return 0
        elif(escape_function(msg_course_hash_name)==2):
            ask_help(msg_course_hash_name)
                   
        global user_data
        
        to_be_uploaded_institute = user_data[str(msg_course_hash_name.chat.id)]["current_institute"]
        to_be_uploaded_year = user_data[str(msg_course_hash_name.chat.id)]["current_year"]
        to_be_uploaded_block = user_data[str(msg_course_hash_name.chat.id)]["current_block"]
        to_be_uploaded_department = user_data[str(msg_course_hash_name.chat.id)]["current_department"]
        to_be_uploaded_course = user_data[str(msg_course_hash_name.chat.id)]["current_course"]
        to_be_uploaded_course_hash = msg_course_hash_name.text.upper()
        
        # checking 
        global institute_architecture_json

        if to_be_uploaded_institute not in institute_architecture_json:
            institute_architecture_json[to_be_uploaded_institute]={}

        if to_be_uploaded_year not in institute_architecture_json[to_be_uploaded_institute]:
            institute_architecture_json[to_be_uploaded_institute][to_be_uploaded_year] = {}

        if to_be_uploaded_block not in institute_architecture_json[to_be_uploaded_institute][to_be_uploaded_year]:
            institute_architecture_json[to_be_uploaded_institute][to_be_uploaded_year][to_be_uploaded_block]={}

        if to_be_uploaded_department not in institute_architecture_json[to_be_uploaded_institute][to_be_uploaded_year][to_be_uploaded_block]:
            institute_architecture_json[to_be_uploaded_institute][to_be_uploaded_year][to_be_uploaded_block][to_be_uploaded_department]={}

        # overwrites if there was a hash to to_be_uploaded_course before..
        institute_architecture_json[to_be_uploaded_institute][to_be_uploaded_year][to_be_uploaded_block][to_be_uploaded_department][to_be_uploaded_course] = to_be_uploaded_course_hash

        course_content_json[to_be_uploaded_course_hash]={}

        # log_content_start
        print()
        print(ist_now())

        print(str(msg_course_hash_name.chat.id)+" created following architecture:")
        print(user_data[str(msg_course_hash_name.chat.id)])

        # log_content_end
        print()

        
        msg = bot.send_message(msg_course_hash_name.chat.id, "(ARCHITECT MODE)Done\nEnter the department name under which Ypu wish to create a new course(It could be new departmrnt or a previously created departmrnt)\nOR\nSend DONE to stop and exit the ARCHITECT MODE.")
        bot.register_next_step_handler(msg, ask_course_name__up)
        
    except Exception:
        traceback.print_exc()
        bot.send_message(
            800851598, "Runtime almost crashed, check the console for traceback!!"
            
            )
        
        bot.send_message(
            msg_course_hash_name.chat.id,
            "Looks like you gave wrong input :P\nSend /help to know what I understand.\n Starting over again\n"
            )


#........................ architect section ends ............................................................


#........................ marketer section starts ............................................................
global_caption = ""
@bot.message_handler(func=valid_marketer)
def reques_to_send_caption(message):
    msg = bot.send_message(message.chat.id,"send the caption(smaller that 1024 chars)!")
    bot.register_next_step_handler(msg, reques_to_send_photo)
    


def reques_to_send_photo(message):
    global global_caption
    global_caption = message.text
    msg = bot.send_message(message.chat.id,"Send only one photo!")
    bot.register_next_step_handler(msg, message_all_)
    # msg

def message_all_(message):
    count=0
    global global_caption
    file_id = message.photo[0].file_id

    if(len(global_caption)<=1024):
        for id in user_data:
            count+=1
            bot.send_photo(chat_id=int(id),photo=file_id ,caption=f"Hi {user_data[id]['firstName']}, {global_caption}")
    else:
        for id in user_data:
            count+=1
            bot.send_message(chat_id=int(id), text=global_caption)  
            bot.send_photo(chat_id=int(id),photo=file_id )        
    bot.send_message(800851598, "Num of people sent:"+str(count))
    global_caption = ""

    # log_content_start
    print()
    print(ist_now())
    print(str(message.chat.id)+" marketed following:")
    print(f'file_id:\n{file_id} \ncaption:')

    print(global_caption)
    # log_content_end

    print()
#........................ marketer section ends ............................................................

#........................ Misc section starts ............................................................


def command_redirector(message):
    if message.text =="/start":
        send_welcome(message)
    elif message.text =="/restart":
        send_welcome(message)
    elif message.text =="/edit_profile":
        edit_profile(message)
    elif message.text =="/feedback":
        ask_feedback(message)
    elif message.text =="/is_bot_live":
        bot.send_message(message.chat.id,"Bot is live right now.\nhttps://allresoursesbot--1paper1pen.repl.co/")
    else:
        ask_help(message)

@bot.message_handler(func=validgreetings)
def sayHiBack(message):
    message
    print(message.from_user.first_name+": "+message.text)
    bot.send_message(message.chat.id,
                     "Hi " + message.from_user.first_name + "!")

def escape_function(message):
    if(message.text == "/escape"):
        bot.send_message(chat_id=message.chat.id,text= "Exited back to normal user mode")
        return 1
    elif(message.text == "/ask_help"):
        return 2        
    return 0

        
def resave_institute_architecture(message):
    out_file = open("institute_architecture.json", "w")
    json.dump(institute_architecture_json, out_file, indent = 4)
    out_file.close()
    bot.send_message(message.chat.id, "Saving success.\nSend the uploader code if you want to enter ADMIN MODE as admin, \nOr you can /start to download content as a user ")

def resave_course_content(message):
    out_file = open("course_content.json", "w")
    json.dump(course_content_json, out_file, indent = 4)
    out_file.close()
    bot.send_message(message.chat.id, "Saving success.\nSend the uploader code if you want to enter ADMIN MODE as admin, \nOr you can /start to download content as a user ")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # files = {"document":open("ss.zip","rb")}
    if message.text in ['Accept Completely and Upload(1)', 'Upload after mannual edit(0.5)', 'Reject Completely(0)']:
        return 0
    print(message.from_user.first_name+": "+message.text)
    bot.send_message(
        message.chat.id,
        "OOPS! I didn't get that.\nYou may also: \n/restart\n/ask_help\n"
        )
    ask_help(message)

keep_alive.keep_alive()
bot.infinity_polling()
