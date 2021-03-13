#!/usr/bin/python3

import argparse
import json
import requests
from typing import Dict

API_URL = 'https://api.vlr.gg'
API_TOKEN = 'bc6fd21d-a09d-4f33-b71b-2223f59711cd'

"""
Methods for hitting Valorant APIs
"""

def get_matchlist(event_id: str) -> Dict:
    resp = requests.get('{API_URL}/matchlist/{event_id}'.format(API_URL=API_URL, event_id=event_id),
                        params={'token': API_TOKEN})
    return resp.json()

def get_match(match_id: str) -> Dict:
    resp = requests.get('{API_URL}/match/{match_id}'.format(API_URL=API_URL, match_id=match_id),
                        params={'token': API_TOKEN})
    return resp.json()

def get_matchlist_main(args: argparse.Namespace) -> None:
    matchlist_json = get_matchlist(args.event_id)
    pretty_json = json.dumps(matchlist_json, sort_keys=True, indent=4)
    print(pretty_json)

def get_match_main(args: argparse.Namespace) -> None:
    match_json = get_match(args.match_id)
    pretty_json = json.dumps(match_json, sort_keys=True, indent=4)
    print(pretty_json)

def create_thread_main(args: argparse.Namespace) -> None:
    match_json = get_match(args.match_id)
    output = ''
    startAtk = True

    # Overall Details
    teams = match_json['teams']
    output += '### ' + teams[0]['name'] + ' ' + teams[0]['maps_won'] + '-' + teams[1]['maps_won'] + ' ' + teams[1]['name']
    output += '\n\n'
    for each_map in match_json['maps']:
        assert each_map['teams'][0]['team_id'] == teams[0]['team_id'] # Assert scores will be ordered correctly
        assert each_map['teams'][1]['team_id'] == teams[1]['team_id']
        output += '**' + each_map['name'].capitalize() + '**: ' + each_map['teams'][0]['rounds_won'] + '-' + each_map['teams'][1]['rounds_won']
        output += '\n\n'
    output += '---\n'

    # Map Details
    for i, each_map in enumerate(match_json['maps'], start=1):
        if i > int(teams[0]['maps_won']) + int(teams[1]['maps_won']): # Don't print third map stats if not played
            break

        # Figure out which side starts first
        if each_map['teams'][0]['rounds_won_atk'] + each_map['teams'][1]['rounds_won_def'] == 12:
            startAtk = True
        else:
            startAtk = False

        # Output round totals per side
        output += '### Map ' + str(i) + ': ' + each_map['name'].capitalize() + '\n\n'
        if startAtk: 
            output += 'Team|ATK|DEF|Total\n'
            output += '---|---|---|---\n'
            output += '**' + each_map['teams'][0]['name'] + '**|'+ str(each_map['teams'][0]['rounds_won_atk']) + '|' + str(each_map['teams'][0]['rounds_won_def']) + '|' + str(each_map['teams'][0]['rounds_won']) + '\n'
            output += '&nbsp;|**DEF**|**ATK**|&nbsp;\n'
            output += '**' + each_map['teams'][1]['name'] + '**|'+ str(each_map['teams'][1]['rounds_won_def']) + '|' + str(each_map['teams'][1]['rounds_won_atk']) + '|' + str(each_map['teams'][1]['rounds_won']) + '\n\n'
        else: 
            output += 'Team|DEF|ATK|Total\n'
            output += '---|---|---|---\n'
            output += '**' + each_map['teams'][0]['name'] + '**|' + str(each_map['teams'][0]['rounds_won_def']) + '|' + str(each_map['teams'][0]['rounds_won_atk']) + '|' + str(each_map['teams'][0]['rounds_won']) + '\n'
            output += '&nbsp;|**ATK**|**DEF**|&nbsp;\n'
            output += '**' + each_map['teams'][1]['name'] + '**|'+ str(each_map['teams'][1]['rounds_won_atk']) + '|' + str(each_map['teams'][1]['rounds_won_def']) + '|' + str(each_map['teams'][1]['rounds_won']) + '\n\n'

        # Output player stat tables
        for each_team in each_map['teams']:
            output += each_team['name'] + '|ACS|K|D|A\n'
            output += '---|---|---|---|---\n'
            for each_player in each_team['players']:
                stats = each_player['stats']
                output += '[' + each_player['alias'] + '](https://www.vlr.gg/player/' + each_player['player_id'] + ') **' + stats['agent'].capitalize() + '**|' + stats['combat_score'] + '|' + stats['kills'] + '|' + stats['deaths'] + '|' + stats['assists'] + '\n'
            output += '\n'
        output += '---\n'

    print(output)

def main():
    parser = argparse.ArgumentParser(description='Post-match thread script',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    sub = parser.add_subparsers()

    get_matchlist_p = sub.add_parser('get_matchlist',
                                     description='Print out matchlist of event')
    get_matchlist_p.add_argument('--event_id',
                                 help='Event Id according to api.vlr.gg',
                                 required=True)
    get_matchlist_p.set_defaults(func=get_matchlist_main)

    get_match_p = sub.add_parser('get_match',
                                 description='Print out match response')
    get_match_p.add_argument('--match_id',
                             help='Match Id according to api.vlr.gg',
                             required=True)
    get_match_p.set_defaults(func=get_match_main)

    create_thread_p = sub.add_parser('create_thread',
                                     description='Print out post match thread')
    create_thread_p.add_argument('--match_id',
                                 help='Match ID according to api.vlr.gg',
                                 required=True)
    create_thread_p.set_defaults(func=create_thread_main)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
