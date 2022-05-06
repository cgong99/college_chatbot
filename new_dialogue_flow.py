
from enum import Enum, auto
from typing import Union, Set, List, Dict, Callable, Tuple, NoReturn
from emora_stdm.state_transition_dialogue_manager.dialogue_flow import *
from emora_stdm.state_transition_dialogue_manager.natex_nlg import NatexNLG
from emora_stdm.state_transition_dialogue_manager.state import State
from NewNatexNLG import *

'''
Override NLG using NewNatexNLG since link cannot be printed
'''
class NewDialogueFlow(DialogueFlow):
    def add_system_transition(self, source: Union[Enum, str, tuple], target: Union[Enum, str, tuple],
                                natex_nlg: Union[str, NewNatexNLG, List[str]], **settings):
            source, target = module_source_target(source, target)
            source = State(source)
            target = State(target)
            if self.has_transition(source, target, Speaker.SYSTEM):
                raise ValueError('system transition {} -> {} already exists'.format(source, target))
            natex_nlg = NewNatexNLG(natex_nlg, macros=self._macros)
            if not self.has_state(source):
                self.add_state(source)
            if not self.has_state(target):
                self.add_state(target)
            self._graph.add_arc(source, target, Speaker.SYSTEM)
            self.set_transition_natex(source, target, Speaker.SYSTEM, natex_nlg)
            transition_settings = Settings(score=1.0)
            transition_settings.update(**settings)
            self.set_transition_settings(source, target, Speaker.SYSTEM, transition_settings)
            if self._all_multi_hop:
                self.update_state_settings(source, system_multi_hop=True)
            if target in self._prepends:
                prepend = self._prepends[target]
                natex = self.transition_natex(source, target, Speaker.SYSTEM)
                self.set_transition_natex(source, target, Speaker.SYSTEM, prepend + natex)
                
    def set_transition_natex(self, source, target, speaker, natex):
        source, target = module_source_target(source, target)
        source = State(source)
        target = State(target)
        if isinstance(natex, str):
            if speaker == Speaker.USER:
                natex = NatexNLU(natex, macros=self._macros)
            else:
                natex = NewNatexNLG(natex, macros=self._macros)
        self._graph.arc_data(source, target, speaker)['natex'] = natex
        
    def update_state_settings(self, state, **settings):
        state = module_state(state)
        state = State(state)
        if 'settings' not in self._graph.data(state):
            self._graph.data(state)['settings'] = Settings()
        if 'global_nlu' in settings:
            self.add_global_nlu(state, settings['global_nlu'])
        if 'enter' in settings and isinstance(settings['enter'], str):
            settings['enter'] = NewNatexNLG(settings['enter'], macros=self._macros)
        self.state_settings(state).update(**settings)