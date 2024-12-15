import requests
from os import environ
from datetime import datetime

KEY = environ['RECAPI']
auth_header = {'Authorization' : 'Bearer ' + KEY}

def teamInfo(teamNo):
    r = requests.get(f'https://www.robotevents.com/api/v2/teams?number%5B%5D={teamNo}&myTeams=false', headers = auth_header)
    data = r.json()['data'][0]
    id = data['id']
    teamName = data['team_name']
    robotName = data['robot_name']
    school = data['organization']
    location = data['location']['city'] + ', ' + data['location']['region']
    return {'id' : id, 'teamName' : teamName, 'robotName' : robotName, 'school' : school, 'location': location}
            

def recentEvents(id):
    thisYear = str(datetime.now().year) + '-01-01'
    nextYear = str(datetime.now().year + 1) + '-12-31'
    r = requests.get(f'https://www.robotevents.com/api/v2/teams/{id}/events?start={thisYear}&end={nextYear}', headers = auth_header)
    data = r.json()['data']
    eventList = []
    for i in range(1, len(data)+1):
        
        currentEvent = data[-i]
        location = currentEvent['location']['venue'] + ', ' + currentEvent['location']['city'] + ', ' + currentEvent['location']['region']
        
        divisions = []
        for division in currentEvent['divisions']:
            divisions.append(division['id'])
            
        eventList.append( {'id' : currentEvent['id'], 'name' : currentEvent['name'], 'date' : currentEvent['start'][:10], 'location' : location, 'divisions': divisions, 'ongoing' : currentEvent['ongoing'], 'startTimestamp': currentEvent['start']} )
    return eventList

def getCurrentEvent(eventList):
    for event in eventList:
        if event['ongoing'] == True:
            return event
    return False

def getMatches(event, teamNum):
    eventID = event['id']
    for divID in event['divisions']:
        r = requests.get(f'https://www.robotevents.com/api/v2/events/{eventID}/divisions/{divID}/matches', headers = auth_header)
        matches = r.json()['data']
        applicableMatches = []
        for match in matches:
            for alliance in match['alliances']:
                for team in alliance['teams']:
                    if team['team']['name'] == teamNum: #for loop bigger than the looooooow taper fade
                        team['team']['name'] = '*'+team['team']['name']+'*'
                        alliances = match['alliances']
                        blueAlliance = ( alliances[0]['teams'][0]['team']['name'] + ', ' + alliances[0]['teams'][1]['team']['name'] ) #First alliance is always blue
                        redAlliance = ( alliances[1]['teams'][0]['team']['name'] + ', ' +  alliances[1]['teams'][1]['team']['name'] ) #First alliance is always blue
                        usefulMatch = { 'name' : match['name'], 'scheduled' : match['scheduled'][11:16],  'field' : match['field'], 'blueAlliance' : blueAlliance, 'redAlliance' : redAlliance}
                        applicableMatches.append(usefulMatch) 
    return applicableMatches

teamNum = '5501B' #input('Team Number: ').upper()
info = teamInfo(teamNum) #5501B is 85868
eventList = recentEvents(info['id'])

matches = getMatches(eventList[1], teamNum)
