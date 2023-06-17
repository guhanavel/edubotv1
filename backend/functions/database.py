import os
import json

#import the requried modules
import firebase_admin
from firebase_admin import db, credentials
from functions.prompt import PROMPT



#authenticate to firebase
cred = credentials.Certificate("db.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://eduflare-9f4c5-default-rtdb.asia-southeast1.firebasedatabase.app/"})



# Save messages for retrieval later on
def get_recent_messages():

  # Define the file name
  ##file_name = "stored_data.json"
  learn_instruction =  {"role": "system", 
                        "content": PROMPT}
  # placeholder first question
  first_question = {"role": "user", 
                    "content": "안녕하세요 이름이 뭐예요? (Annyeonghaseyo, ireumi mwoyeyo?)"}
  # Initialize messages
  messages = []


  # Append instruction to message
  messages.append(learn_instruction)
  messages.append(first_question)

  # Get last messages from database
  try:
    ref = db.reference("/history").get()

    # Append last 5 rows of data
    if ref:
      if len(ref) < 5:
        for item in ref:
          messages.append(item)
      else:
        for item in ref[-5:]:
          messages.append(item)
  except:
    pass

  
  # Return messages
  return messages


# Save messages for retrieval later on
def store_messages(request_message, response_message):

  # Define the file name
  file_name = "stored_data.json"

  # Get recent messages
  messages = get_recent_messages()[1:]

  # Add messages to data
  user_message = {"role": "user", 
                  "content": request_message}
  assistant_message = {"role": "assistant", 
                       "content": response_message}
  messages.append(user_message)
  messages.append(assistant_message)

  # Save the data into firebase
  db.reference("/").update({"history":messages})


# Save messages for retrieval later on
def reset_messages():


  # reset message from firebase
  db.reference("/").delete()
  # append learning instruction into firebase db
  db.reference("/").update({"role": "system", 
                        "content": "You are a Korean teacher and your name is Jeadok, the user are students taking Korean module. They will be using you to practise their conversation.Keep responses under 20 words. content from school slides These are the lesson materials for lesson 1: Slide 1: 무엇을 공부합니까? 제 1과 저는 회사원입니다, 1. 새 어휘: 직업, 2. 새 문법: ‐입니다,‐입니까? ,‐습니다,‐습니까?, Slide 2: 어휘: , Slide 3: 문법: -입니다, -입니까?, With a picture of a Kpop band: , 안녕하세요?, 에이핑크예요. ,저는 정은지예요.,저는 오하영이에요., 여러분, 만나서 반가워요!. You are limited to using content from these and your response should only be in Korean. In addition whenever the conversation goes out of scope, bring the user back to the lesson",
                        "history":[]})

