# state for each of the residence hall?
from emora_stdm import DialogueFlow, Macro
import json

hall_names = {"alabama", "complex", "eagle", 
              "hamilton holmes", "raoul", "turman", "dobbs", "haris"}

rates = {
  "alabama" : 100
}

housing_options_phrase = {"options", "dorms", "residence hall"}
rates_info = {
  'double' : '4,835',
  'single' : '5,301',
  'triple' : '4,658',
  'super single' : '6,370'
}



class CATCH_HALL_OPTIONS(Macro):
  def __init__(self):
    pass
  
  def run(self, ngrams, vars, args):
    pass



class CATCH_HALL(Macro):
  def __init__(self):
      """hall name list"""
      self.halls = hall_names

  def run(self, ngrams, vars, args):
      """Performs operation"""
      
      return ngrams & self.halls


class GET_ROOM_TYPE(Macro):
  def __init__(self):
    print("****** initialize GET ROOM TYPE ******")
    self.room_types = set(rates_info.keys()) 
  
  def run(self, ngrams, vars, args):
    print('**** GEt Room *****')
    # print(vars)
    # print("\n")
    # print(args)
    print(ngrams & self.room_types)
    return ngrams & self.room_types



class GET_RATES(Macro):
  def __init__(self):
    self.rates = rates_info
  
  def run(self, ngrams, vars, args):
    print('**** GET Rates *****')

    room = vars[args[0]]
    return self.rates[room]

    



class GENERATE_HALL_RESPONSE(Macro):
  def __init__(self):
      """Inits CATCH with list"""
      self.halls = hall_names

  def run(self, ngrams, vars, args):
      """Performs operation"""
      res = "\n"
      rate = rates[vars[args[0]]]
      return rate


class RETURN_HALL_LIST(Macro):
  def __init__(self):
      self.halls = hall_names

  def run(self, ngrams, vars, args):
    res = ""
    for name in self.halls:
      res = res + "\n" + name + " hall"
    return res
    



class LOCATION(Macro):
  def __init__(self, path):
    self.path = path
    with open(self.path, 'r') as f:
      self.db = json.load(f)

  def run(self, ngrams, vars, args):
    # input hall name
    # print(args[0])
    # print(vars[args[0]])

    location = self.db[vars[args[0]]]['Location']
    return location


class CONTACT_HALL(Macro):
  def __init__(self, path):
    self.path = path
    with open(self.path, 'r') as f:
      self.db = json.load(f)

  def run(self, ngrams, vars, args):
    # input hall name
    hall = vars[args[0]]
    staff = self.db[hall]['Staff']
    staff_name = list(staff.keys())[0]
    title = staff[staff_name]['title']
    email = staff[staff_name]['email']
    res = "Here is the contact information of " + staff_name + ", " + title +"\nemail: "+email
    return res


class FLOOR_PLAN(Macro):
  def __init__(self, path):
    self.path = path
    with open(self.path, 'r') as f:
      self.db = json.load(f)

  def run(self, ngrams, vars, args):
    # input hall name
    hall_name = vars[args[0]]
    hall = self.db[hall_name]
    room_info = hall['rooms']
  
    res = room_info['type'] + " are offered at " + hall_name + ".\n"
    all_link = hall["Floor Plan Link"]
    res += "Here are the links to different floor plans of "+ hall_name +":\n"
    for type in all_link.keys():
      res = res + "\n"+ type + ": `" + all_link[type]+"`"
    return res



class AMENITIES(Macro):
  # generate amenities response to each specific hall
  def __init__(self, path):
    self.path = path
    with open(self.path, 'r') as f:
      self.db = json.load(f)
    
    def run(self, ngrams, vars, args):
      """use arguments to query for data"""
      hall_name = vars[args[0]]
      hall = self.db[hall_name]
      room_info = hall['rooms']
      bed = self.db['general info'][bed]
      
      pass
    

class MOVEIN(Macro):
  def __init__(self, path):
    self.path = path
    with open(self.path, 'r') as f:
      self.db = json.load(f)
      
  def run(self, ngrams, vars, args):
    """use arguments to query for data"""
    return self.db['general info']["move in"]

class MOVEOUT(Macro):
  def __init__(self, path):
    self.path = path
    with open(self.path, 'r') as f:
      self.db = json.load(f)
      
  def run(self, ngrams, vars, args):
    """use arguments to query for data"""
    return self.db['general info']["move out"]