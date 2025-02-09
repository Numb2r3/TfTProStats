from urllib.error import HTTPError
from urllib.request import urlopen
import json
from dotenv import load_dotenv
import os

class RiotApiError(Exception):
    def __init__(self, message):
        super().__init__(message)

search_name = ['puuid','gameName','summonerId']
search_option =['account','summoner','league',]
available_regions = ['europe','americas','asia','esport','ru','br1','euw1','eun1','la1','la2','me1','na1','la2','tr1']


key = '?api_key=RGAPI-ee5fa6dd-0912-4a3c-81dc-25e0d1ce7bd2'

def get_api(**kwargs):
    api_string = ''

    if 'region' in kwargs:
        if kwargs['region'] in available_regions:
            api_string = 'https://' + kwargs['region'] + '.api.riotgames.com'
        else:
            raise RiotApiError('Region error: given region is not available')
    else:
        raise RiotApiError('Region error: no region given')


    if 'search_option' not in kwargs:
        raise RiotApiError('Search error: no search option given')

    if kwargs['search_option'] in search_option:
        match kwargs['search_option']:
            case 'account':
                api_string = api_string + '/riot/account/v1/accounts' 
                
            case 'summoner':
                api_string = api_string + '/lol/summoner/v4/summoners'

            case 'league':
                api_string = api_string + 'tft/league/v1/entries'
            case _:
                RiotApiError('Search error: no available search option')
    

    ## hier muss dot env umgebung rein und es muss behandelt werden das der key nichtmehr ans ende des strings kommt
    if 'search_name' not in kwargs:
        raise RiotApiError('Search error: no search id given')
    
    
    if kwargs['search_name'] in search_name:
        match kwargs['search_name']:
            case 'puuid':
                if 'puuid' in kwargs:
                    api_string = api_string +'/by-puuid/' + kwargs['puuid'] + key
                else:
                    raise RiotApiError('Search error: puuid not given')
            case 'summonerId':
                if 'summonerId' in kwargs:
                    api_string = api_string + '/by-summoner/' + kwargs['summonerId'] + key
                else:
                    raise RiotApiError('Search error: summonerId not given')
            case 'gameName':
                if 'gameName' in kwargs and 'tagLine' in kwargs:
                    api_string = api_string + '/by-riot-id/' + kwargs['gameName'] + '/' + kwargs['tagLine'] + key
                else:
                    raise RiotApiError('Search error: gameName or tagLine not given')
            case _:
                raise RiotApiError('Search error: no available search name')

    return api_string

def load_account(**kwargs):
    defaultkwargs = {'region':'europe'}
    kwargs = {**defaultkwargs,**kwargs}

    if 'puuid' in kwargs:

        api_string = get_api(region = kwargs['region'],
                             search_option = 'account',
                             search_name = 'puuid',
                             puuid = kwargs['puuid']
                             )
        return json.loads(urlopen(api_string).read())
    
    if 'gameName' in kwargs:
        if 'tagLine' in kwargs:
            api_string = get_api(region = kwargs['region'],
                                 search_option = 'account',
                                 search_name = 'gameName',
                                 gameName = kwargs['gameName'],
                                 tagLine = kwargs['tagLine'] )
            return json.loads(urlopen(api_string).read())
        else:
            raise RiotApiError ('load account error: tagLine missing')
        
    else:
        raise RiotApiError( 'load account error: no search parameter given')
    
    return

def load_summonerId(region,puuid):
    if region not in available_regions:
        raise RiotApiError('load summonerId error: no available region')
    
    try:
        api_string = get_api(region = region,
                            search_option = 'summoner',
                            search_name = 'puuid',
                            puuid = puuid)
        print(api_string)
        return json.loads(urlopen(api_string).read())
    
    except RiotApiError:
        return RiotApiError