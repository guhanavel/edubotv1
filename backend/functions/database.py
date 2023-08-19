import os
import json

#import the requried modules
import firebase_admin
from firebase_admin import db, credentials
from functions.prompt import PROMPT, QNS_1



#authenticate to firebase
cred = credentials.Certificate("db.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://eduflare-9f4c5-default-rtdb.asia-southeast1.firebasedatabase.app/"})

def template():

  # Define the file name
  ##file_name = "stored_data.json"
  messages =  [{
      "role":"system",
      "content": "###Limit: Make your response at most 20 words. and stop when ### Count == 4. each time increase ### Count by 1. \
      ### Kill-Switch: When a user goes out of topic, or ask weird questions more than 2 counts or the conversation has reached 6 counts. End the conversation by saying Thank you and add this back <End of conversation> \
      ### Role: User: A person curious about different professions. AI: A career counselor discussing various professions. \
      ### Situation: Role:User: A tourist looking for transportation advice. AI: A local guide familiar with the transportation system. Prompt: Inform the user about the diverse transportation options available in Seoul. Offer insights into routes, costs, and the conveniences of each mode. Direct them to use the grammar concepts; 으로/로 에서-까지 (-Towards, By, From-to) when asking about different modes of transportation.  \
      ### Feedback: Based on the user content, give feedback on how is the response and any area for improvement. Also point out any errors."
      },
	      {
            "role": "assistant",
            "content": "안녕하세요! 만나서 반갑습니다. ### Count: 1 ### Feedback: {Write feedback here if any}"
        },
	]
  # Return messages
  return messages


def get_recent_messages():

  # Initialize messages
  messages = template()


  # Get last messages from database
  try:
    ref = db.reference("/history").get()

    # Append last 5 rows of data
    if ref:
        for item in ref:
          messages.append(item)
  except:
    pass

  # Return messages
  return messages

# Save messages for retrieval later on



# Save messages for retrieval later on
def store_messages(request_message, response_message):

  # Define the file name
  #file_name = "stored_data.json"

  # Get recent messages
  messages = get_recent_messages()

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
                        "content": "###Limit: Make your response at most 20 words. and stop when ### Count == 4. each time increase ### Count by 1. \
      ### Kill-Switch: When a user goes out of topic, or ask weird questions more than 2 counts or the conversation has reached 6 counts. End the conversation by saying Thank you and add this back <End of conversation> \
      ### Role: User: A person curious about different professions. AI: A career counselor discussing various professions. \
      ### Situation: Engage the user by asking them about their interests and aspirations. Introduce them to various occupations, discussing the nature of each job, their pros and cons, and the qualifications required. Encourage the user to inquire and respond using the formal endings -입니다, -입니까? and -습니다, -습니까? . \
      ### Feedback: Based on the user content, give feedback on how is the response and any area for improvement. Also point out any errors.",
                        "history":[]})

