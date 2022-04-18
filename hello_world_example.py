
import imp
from emora_stdm import DialogueFlow
from emora_stdm import NatexNLG
from NewNatexNLG import *

chatbot = DialogueFlow('start')
transitions = {
    'state': 'start',
    '"Hello. How are you?"': {
        '[{good, okay, fine}]': {
            '"Good. I am doing well too."': {
                'error': {
                    '"See you later!"': 'end'
                }
            }
        },
        'error': {
            '"Well I hope your day gets better!"': {
                'error': {
                    '"Bye!"': 'end'
                }
            }
        }
    }
}
chatbot.load_transitions(transitions)

if __name__ == '__main__':
    # chatbot.run(debugging=True)
    # natex_nlg = NatexNLG('"hi there" `$500`')
    natex_nlg = NatexNLG("hi there `https://www.hi.com`")
    natex_link = NewNatexNLG("Building Floor Plan`https://housing.emory.edu/i_ncludes`")
    print(natex_link.generate(debugging=True))
    print(natex_nlg.generate(debugging=False))
    # natex_nlg = NatexNLG('#SET($is_adult=True)')
    # print(natex_nlg.generate(debugging=False))