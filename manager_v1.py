
from emora_stdm import CompositeDialogueFlow,DialogueFlow,Macro
from new_dialogue_flow import *
import sys
sys.path.append('/Users/gongchen/Emora/emora_stdm')
from enum import Enum
from marco import *

from transitions import *


# use for multiple flows
# cdf = CompositeDialogueFlow('start', 'topic_err', 'topic', initial_speaker=DialogueFlow.Speaker.USER)


# single flow
housing_info_path = "housing_info.json"

class State():
  START = "start"
  BEGIN = "begin"
  RESTART = "restart"
  ERROR_RESTART = "error_restart"
  RATES = "rates"
  CONTACT = "contact"
  CONTACT_ASKHALL = "contact_askhall"
  CONTACTBEGIN = "contactbegin"
  MOVEIN = 'move_in'
  MOVEOUT = 'move_out'
  HOUSING_GENERALL = 1
  HALL_OPTIONS = "housing_options"
  INTRO_HALLS = "intro_hall"
  HOUSING_HALL = 3
  HALL_OPTIONS_ANSWER = 4

  


macros = {
  "CATCH_HALLS": CATCH_HALL(),
  "GENERATE_HALL_RESPONSE": GENERATE_HALL_RESPONSE(),
  "GET_ROOM_TYPE": GET_ROOM_TYPE(),
  "GET_RATES": GET_RATES(),
  "RETURN_HALL_LIST": RETURN_HALL_LIST(),
  "LOCATION": LOCATION(housing_info_path),
  "CONTACT_HALL": CONTACT_HALL(housing_info_path),
  "FLOOR_PLAN": FLOOR_PLAN(housing_info_path),
  "MOVEIN": MOVEIN(housing_info_path),
  "MOVEOUT": MOVEOUT(housing_info_path),
}

#Use new DialogueFlow for free output format
df = NewDialogueFlow(State.START, initial_speaker=DialogueFlow.Speaker.SYSTEM, macros=macros)





standard_opening = '"Hi this is Emory Housing. How can I help you?" #SET($hall_selected=False)'
restart = '"\nWhat else can I help you?"'
error_restart = '"\nSorry I am not understanding the questions. Can I help you with other things?"'




# START/RESTART -> BEGIN
df.add_system_transition(State.START, State.BEGIN, standard_opening)
df.add_system_transition(State.RESTART, State.BEGIN, restart)
df.add_system_transition(State.ERROR_RESTART, State.BEGIN, error_restart)


# USER QUESTIONS
# 1. asking hall optinos
df.add_user_transition(State.BEGIN, State.HALL_OPTIONS, '[what, {housing, options}]')
# 2. housing rates/ costs/ fee/ .....
df.add_user_transition(State.BEGIN, State.RATES, '[{rates, fee, cost}]')
# 3. Date move in/out
df.add_user_transition(State.BEGIN, State.MOVEIN, '{[move, in] date}')
df.add_user_transition(State.BEGIN, State.MOVEOUT, '{[move, out] date}')
# 4. Application
# 5. Contacts
df.add_user_transition(State.BEGIN, State.CONTACTBEGIN, '[{contact, contacts, number}]')
# 6. Hall amenities
# 7. Room amenities/ Floor plan

# specific hall
df.add_user_transition(State.BEGIN, State.INTRO_HALLS,'[$preferred_hall=#CATCH_HALLS(), #SET($hall_selected=True)]')

df.set_error_successor(State.BEGIN, State.ERROR_RESTART)


# STORE QUESTION, COMFIREM HALL, use if check preferred hall
# SET preferred hall xxxx , transite to corresponding xxx

# CONTACT check if hall_selected 
df.add_system_transition(State.CONTACTBEGIN, State.CONTACT, '#IF($hall_selected=False)')
df.add_system_transition(State.CONTACTBEGIN, State.CONTACT_ASKHALL, '#IF($hall_selected=True)')

df.add_system_transition(State.CONTACT_ASKHALL, State.CONTACT_ASKHALL, '"The contact informaiton varies from different halls. Which hall do you want to know?"')
df.add_user_transition(State.CONTACT_ASKHALL, State.CONTACT, '[$preferred_hall=#CATCH_HALLS(), #SET($hall_selected=True)]')
df.set_error_successor(State.BEGIN, State.ERROR_RESTART)


# MOVE IN/OUT DATE
df.add_system_transition(State.MOVEIN, State.BEGIN, '#MOVEIN()')
df.add_system_transition(State.MOVEOUT, State.BEGIN, '#MOVEOUT()')



# SYSTEM
# df.add_system_transition(State.HALL_OPTIONS, State.HALL_OPTIONS_ANSWER, "There are 8 residence halls for first year students. #GENERATE_HALL_RESPONSE()")
# df.load_transitions(ask_rates) # RATES
# df.add_system_transition("rates", State.START, ask_rates)
# residenthall state

# USER CATCH PREFERRED HALL
# df.add_user_transition(State.HALL_OPTIONS_ANSWER, State.HALL_OPTIONS_ANSWER, '[$preferred_hall=#CATCH_HALLS()]')

# go to each housing branch. or pass hall as a variable



if __name__ == '__main__':
    # automatic verification of the DialogueFlow's structure (dumps warnings to stdout)
    df.check()
    df.precache_transitions()
    df.load_transitions(ask_rates)
    df.load_transitions(housing_options)
    df.load_transitions(intro_hall)
    # df.load_transitions(transitions)
    # run the DialogueFlow in interactive mode to test
    df.run(debugging=False)
