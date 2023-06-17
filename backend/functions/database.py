import os
import json

#import the requried modules
import firebase_admin
from firebase_admin import db, credentials
from functions.prompt import PROMPT, QNS_1



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
                    "content": QNS_1}
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
                        "content": PROMPT,
                        "history":[]})

