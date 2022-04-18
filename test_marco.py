
from emora_stdm import DialogueFlow
from emora_stdm import NatexNLU, Macro
from marco import *



# single flow
housing_info_path = "housing_info.json"

macros = {
  "CATCH_HALLS": CATCH_HALL(),
  "GENERATE_HALL_RESPONSE": GENERATE_HALL_RESPONSE(),
  "GET_ROOM_TYPE": GET_ROOM_TYPE(),
  "GET_RATES": GET_RATES(),
  "RETURN_HALL_LIST": RETURN_HALL_LIST(),
  "LOCATION": LOCATION(housing_info_path),
  "CONTACT_HALL": CONTACT_HALL(housing_info_path),
  "FLOOR_PLAN": FLOOR_PLAN(housing_info_path)
}



ask_rates = {
  "state": 'rates',
  '"Looks like you want to know the housing rates. Sure, we have 4 different room types: \n Single\n Double \n Triple\n Super Single\n\
  Which one do you want to know about?"':{
    "[$room=#GET_ROOM_TYPE()]": {
      '"The rate for" $room "room would be" #GET_RATES(room) "dollars per semester."': {
        "error": 'rates'
      }
    },
    'error' : {
      '"Sorry I don\'t quite understand that."' : "end"
    }
  }
}

intro_hall = {
  "state": 'intro_hall',
  '"What do you want to know more about?"':{
    '[{where, location}]':{
      '"Here is the location: " #LOCATION(preferred_hall) "\n What else can I help you?"': 'start'
    },
    '[{contact, contacts, number}]':{
      '#CONTACT_HALL(preferred_hall)':'start'
    },
    '[{floor, [floor, plan], [rooms, look, like]}]': {
      '#FLOOR_PLAN(preferred_hall)': 'start'
    },
    'error': {
      '"Sorry I don\'t know about this information."' : 'intro_hall'
    }
  }
}

test = {
  "state":'test',
  '"Hello"#SET($preferred_hall=alabama)':{
    '[{floor, plan}]': {
      '#FLOOR_PLAN(preferred_hall)':'end'
    }
  }
}

if __name__ == '__main__':

  chatbot = DialogueFlow('test', initial_speaker=DialogueFlow.Speaker.SYSTEM, macros=macros)
  chatbot.load_transitions(test)
  chatbot.run(debugging=False)

