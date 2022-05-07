housing_options = {
  "state": 'housing_options',
  '"There are 8 residence halls for first year students. " #RETURN_HALL_LIST() "\nWhich one do you want to know more?"': {
    '[$preferred_hall=#CATCH_HALLS()]': 'intro_hall',
    'error': {
      '"Sorry I don\'t think I know this name. Do you want to try another name or say return I can help you with other things?"': {
        '[$preferred_hall=#CATCH_HALLS()]': 'intro_hall',
        'error': 'start'
      }
    }
  }
}

intro_hall = {
  "state": 'intro_hall',
  '"What do you want to know more about" $preferred_hall "hall?\n You can say restart to go back."':{
    '[{where, location}]':{
      "state": 'location',
      '"Here is the location: " #LOCATION(preferred_hall) "\n"' : 'intro_hall'
    },
    '[{contact, contacts, number}]':{
      "state" : 'contact',
      '#CONTACT_HALL(preferred_hall)':'intro_hall'
    },
    '[{floor, [floor, plan], [rooms, look, like]}]': {
      "state":'floor_plan',
      '#FLOOR_PLAN(preferred_hall)': 'intro_hall'
    },
    '{furniture, amenities, amenity}' : {
      "state":'amenities',
      '#AMENITY(preferred_hall)' : 'intro_hall'
    },
    'restart' : 'restart',
    'error': {
      '"Sorry I don\'t know about this information."' : 'intro_hall'
    }
  }
}
# ask location
# ask contacts
# ask room amenities
# ask floor amenities

ask_rates = {
  "state": 'rates',
  '"Sure, we have 4 different room types: \n  Single\n  Double \n  Triple\n  Super Single\n\
  Which one do you want to know about?"':{
    "[$room=#GET_ROOM_TYPE()]": {
      '"The rate for" $room "room would be" #GET_RATES(room) "dollars per semester."': 'restart'
    },
    'error' : {
      '"Sorry I don\'t quite understand that."' : "rates"
    }
  }
}


if __name__ == '__main__':
  import json
  path = "housing_info.json"
  path = path
  with open(path, 'r') as f:
    db = json.load(f)

  print(db.keys())
  print(db['alabama'])
  print(db['alabama']['Staff'])
  print(list(db['alabama']['Staff'].keys()))