import requests

api_key = '505D0B21E16FA9900DB3CAC054AC2880'
account_id = '237964995'

# Make API request to retrieve player match history
match_history_url = f'http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?key={api_key}&account_id={account_id}'
match_history_response = requests.get(match_history_url)
match_history_data = match_history_response.json()['result']['matches']

if match_history_data:
    print('Player match history:')
    for match in match_history_data:
        match_id = match['match_id']
        match_date = match['start_time']
        print(f'Match ID: {match_id}, Match Date: {match_date}')

        # Make API request to retrieve match details
        match_details_url = f'http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/?key={api_key}&match_id={match_id}'
        match_details_response = requests.get(match_details_url)
        match_details_data = match_details_response.json()['result']

        # Extract and display statistics from match details
        if match_details_data:
            player_slot = next(
                (player['player_slot'] for player in match_details_data['players'] if player['account_id'] == int(account_id)),
                None
            )
            if player_slot is not None and player_slot < 10:
                player_stats = match_details_data['players'][player_slot]
                kills = player_stats['kills']
                deaths = player_stats['deaths']
                assists = player_stats['assists']
                hero_damage = player_stats['hero_damage']
                tower_damage = player_stats['tower_damage']

                print(f'Kills: {kills}')
                print(f'Deaths: {deaths}')
                print(f'Assists: {assists}')
                print(f'Hero Damage: {hero_damage}')
                print(f'Tower Damage: {tower_damage}')
        print('-' * 20)
else:
    print('Player match history not available.')

# Calculate statistics
total_matches = len(match_history_data)
total_wins = 0

# Make API request to retrieve match details for win rate calculation
match_details_url = f'http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/?key={api_key}'

for match in match_history_data:
    match_id = match['match_id']
    match_details_response = requests.get(f'{match_details_url}&match_id={match_id}')
    match_details_data = match_details_response.json()['result']

    if match_details_data['radiant_win']:
        total_wins += 1

win_rate = (total_wins / total_matches) * 100 if total_matches > 0 else 0

# Print statistics
print(f'Total Matches: {total_matches}')
print(f'Total Wins: {total_wins}')
print(f'Win Rate: {win_rate}%')
