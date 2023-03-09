from bs4 import BeautifulSoup
from time import sleep


def current_moment(time):
    if '1' in time:
        set = 1
    elif '2' in time:
        set = 2
    elif '3' in time:
        set = 3
    else:
        set = 0

    print('SET :: ', set)

    return set

def get_link(match):
    link = match.get_attribute("id")
    url = f"https://www.volleyball24.com/match/{link[5:]}"
    return url

def handling(game):
    match = game.get_attribute("innerHTML")
    soup = BeautifulSoup(match, "html.parser")
    home_team = soup.select_one("div.event__participant.event__participant--home").text.strip()
    away_team = soup.select_one("div.event__participant.event__participant--away").text.strip()
    time = soup.select_one("div.event__stage--block").text.strip().split()
    print(home_team,' - ', away_team)

    score1_1, score1_2, score2_1, score2_2 = 0, 0, 0, 0

    if soup.select_one("div.event__score.event__score--home").text.strip().isdigit() and \
            soup.select_one("div.event__score.event__score--away").text.strip().isdigit():
        score_one = int(soup.select_one("div.event__score.event__score--home").text.strip())
        score_two = int(soup.select_one("div.event__score.event__score--away").text.strip())

        e1_1 = soup.select_one("div.event__part--home.event__part--1")
        e2_1 = soup.select_one("div.event__part--away.event__part--1")
        e1_2 = soup.select_one("div.event__part--home.event__part--2")
        e2_2 = soup.select_one("div.event__part--away.event__part--2")
        e1_3 = soup.select_one("div.event__part--home.event__part--3")
        e2_3 = soup.select_one("div.event__part--away.event__part--3")

        def ex(data): # existance
            if isinstance(data, type(None)):
                return 0
            if data.text.strip().isdigit():
                return int(data.text.strip())
            else:
                return  777

        score1_1, score2_1, score1_2, score2_2 = ex(e1_1), ex(e2_1),ex(e1_2),ex(e2_2)
        score1_3, score2_3 = ex(e1_3), ex(e2_3)

    else:
        score_one = 999
        score_two = 999

    score_line = (score1_1, score2_1, score1_2, score2_2, score1_3, score2_3)
    print(score_line)
    print("DIRTY TIME:: ", time)
    print("CURRENT SCORE:: ", score_one, "-", score_two)

    if "Finished" in time or "Overtime" in time or "Postponed" in time \
            or "Interrupted" in time or "Awaitingupdates" in time or "Awarded" in time:
        time = ["Fin", "Fin"]

    return time, score_one, score_two, score_line


