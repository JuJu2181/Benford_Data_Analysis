from pyramid.config import Configurator 
from views import *

def includeme(config: Configurator) -> None:
    config.add_route('home','/')
    config.add_view(home_view,route_name='home')
    config.add_route('benford','/benford')
    config.add_view(benford,route_name='benford')
    config.add_route('analyse','/analyse')
    config.add_view(benford,route_name='analyse')
    
    
