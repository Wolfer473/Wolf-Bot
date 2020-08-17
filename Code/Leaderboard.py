from json import loads
from discord import Embed
from requests import get
from config import fortniteAPIKey
from BlobheartUserNames import fortniteHandles
from time import sleep
import shlex


def listMaker(ctx):
    cleanStr = ctx.message.content.replace('~leaderboard', '')
    try:
        cleanStr = shlex.split(cleanStr)
    except Exception:
        return cleanStr
    return cleanStr


def generateErrorEmbed():
    errorEmbed = Embed(
        title="Error!",
        description="Invalid Format and/or Username(s)!",
        color=0xde2121
        )
    errorEmbed.set_thumbnail(
        url="https://i.imgur.com/wunfgw0.png"
        )
    errorEmbed.add_field(
        name='Usage:',
        value='~leaderboard \'name1\' \'name2\' \'name3\'',
        inline=True
        )
    return errorEmbed


# Calls getLeaderBoardXP with either pre-set list or added commands
def leaderBoardXPFormat(definedNames):

    if not definedNames:
        nameList = fortniteHandles
        print('Created leaderboard with pre-set Epic Names...')
    else:
        nameList = definedNames
        print('Created leaderboard with name array "{}"...'.format(
            definedNames
            ))

    try:
        scores = (dict(sorted(
            getLeaderBoardXP(nameList).items(),
            key=lambda x: x[1],
            reverse=True
            )))
    except KeyError:
        return generateErrorEmbed()

    names = []
    values = []
    items = scores.items()
    for item in items:
        names.append(item[0]), values.append(item[1])

    scoreEmbed = Embed(
        title="XP Leaderboard",
        color=0x1167b1
    )
    scoreEmbed.set_thumbnail(url='https://i.imgur.com/LIzNl5f.jpg')
    for x in range(len(nameList)):
        scoreEmbed.add_field(
            name='{num})  **{name}**'.format(
                num=(x+1),
                name=names[x]),
            value='>> ' + ('*{}*'.format('{:,}'.format(values[x]) + ' XP')),
            inline=False
        )
    print('Leaderboard Embed created and sent successfully.')
    return scoreEmbed


def getStats(epicName):
    requestURL = (
        'https://api.fortnitetracker.com/v1/profile/all/{name}'
        .format(name=epicName)
        )
    token = fortniteAPIKey
    request = get(url=requestURL, headers=token)
    data = loads(request.text)
    score = data['lifeTimeStats'][6]['value']
    return int(score.replace(',', ''))


# Fetches the info for names in nameList and places them in a Dictionary
def getLeaderBoardXP(nameList):
    scoreboard = {}

    for x in range(len(nameList)):
        scoreboard[nameList[x]] = getStats(nameList[x])
        # Sleep To Prevent API From Invalidating Request
        sleep(1)

    return scoreboard
