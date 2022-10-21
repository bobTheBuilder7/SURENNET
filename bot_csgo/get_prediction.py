from aiohttp import ClientSession
from lxml import html

# from lxml.html.clean import clean_html

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/14.1.1 Safari/605.1.15',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru', 'dnt': '1', "Connection": "keep-alive"}


async def get_bets(tree):
    bets = tree.find_class('odds-cell border-left')
    urls = []
    allBets = []
    coefA = []
    coefB = []
    for i in bets:
        for j in i.iterlinks():
            if urls.count(j[2]) == 3:
                break
            urls.append(j[2])
            allBets.append(j[0].text)
    flag = True
    for i in allBets:
        if i != '-':
            if flag:
                coefA.append(float(i))
                flag = False
            else:
                coefB.append(float(i))
                flag = True
    return coefA, coefB


async def get_winner(model, match_page: str):
    async with ClientSession(headers=headers) as session:
        # # matchId = match_page.split('/')[4]
        # # matchName = match_page.split('/')[5]
        # # async with session.get(f'https://www.hltv.org/betting/analytics/{matchId}/{matchName}') as response:
        async with session.get(match_page) as response:
            content = await response.text()
            tree = html.fromstring(content)

            first_team_id = int([i for i in tree.find_class('team1-gradient')[0].iterlinks()][0][2].split('/')[2])
            first_team_name = tree.find_class('team1-gradient')[0].find_class('teamName')[0].text
            second_team_id = int([i for i in tree.find_class('team2-gradient')[0].iterlinks()][0][2].split('/')[2])
            second_team_name = tree.find_class('team2-gradient')[0].find_class('teamName')[0].text
            id_to_name = {first_team_id: first_team_name, second_team_id: second_team_name}
            coefA, coefB = await get_bets(tree)
            if len(coefA) != 0:
                coefA_avg = round(sum(coefA) / len(coefA), ndigits=2)
                coefB_avg = round(sum(coefB) / len(coefB), ndigits=2)
                if model.predict([[first_team_id, second_team_id, coefA_avg, coefB_avg]]) == [0]:
                    return id_to_name[first_team_id], coefA, coefB, first_team_name, second_team_name
                else:
                    return id_to_name[second_team_id], coefA, coefB, first_team_name, second_team_name
            else:
                return None, None, None, None, None
