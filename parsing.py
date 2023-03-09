from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from functools import reduce
from itertools import chain
import time
from statistics import mean
from send import bet_siska


def check_link(url,time,score_one,score_two,checker,sl):

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(desired_capabilities=caps,options=options)
    browser.get(url)
    browser.implicitly_wait(1)
    team_home = browser.find_elements(By.CSS_SELECTOR, "a.participant__participantName")[0].get_attribute(
        "href") + "results/"
    team_away = browser.find_elements(By.CSS_SELECTOR, "a.participant__participantName")[1].get_attribute(
        "href") + "results/"
    title = browser.find_element(By.CSS_SELECTOR, ".tournamentHeader__country").text

    def separator(matches):
        match_list = list()
        for i in matches:
            line = i.text
            #  print(line)
            if "(" in line or "Awrd" in line or "Abn" in line:
                continue
            if len([i for i in line.split() if i.isdigit()]) < 6:
                continue
            match_list.append(line.split())
        return match_list

    def get_data(browser, link):
        browser.get(link)
        dataset = browser.find_elements(By.CSS_SELECTOR, "[id^='g_12']")
        matches = separator(dataset)
        team = browser.find_element(By.CSS_SELECTOR, "div.heading__name").get_attribute("innerHTML")
        return matches, team

    def forming(browser, link1, link2):  # NEED ADD TYPE SPORT AND FIXABLE CSS SELECTOR
        match_list_home, team1 = get_data(browser, link1)
        match_list_away, team2 = get_data(browser, link2)
        return match_list_home, match_list_away, team1, team2

    games = forming(browser, team_home, team_away)


    team1_name = games[2].split()
    team2_name = games[3].split()


    def separation_home_away(team_, all_matches):
        home_matches = list()
        away_matches = list()
        waste = ["W", "U18", "U19", "U20", "U21", "U23"]  # WASTE - U20 and another juniors and woman champs//
        for i in waste:
            if i in team_:
                team_ = [j for j in team_ if j not in waste]
        print(team_)

        for k in all_matches:
            i = [j for j in k[:len(k) - 1] if j not in waste] + k[-1:]
            x = i.index(team_[len(team_) - 1])
            if i[x + 1].isdigit():
                away_matches.append(i)
            elif "(" in i[x + 1] and i[x + 2].isdigit():
                away_matches.append(i)
            else:
                home_matches.append(i)
        return home_matches, away_matches


    team1_home, team1_away = separation_home_away(team1_name,games[0])
    team2_home, team2_away = separation_home_away(team2_name,games[1])

    for i in team2_away:
        print(i)


    def get_scores(data):

        scoreline = list()

        for match in data:
            one_line = list()
            for scores in reversed(match):

                if scores.isdigit():
                    if int(scores) not in [0, 1, 2, 3]:
                        one_line.append(int(scores))

                    if int(scores) in [0, 1, 2, 3]:
                        break
            if len(one_line) >= 6:
                scoreline.append(one_line)

        def ordered(line):
            real_scoreline = list()
            for i in line:
                real_scoreline.append(i[::-1])
            return real_scoreline

        return ordered(scoreline)

    for i in get_scores(team2_away):
        print(i)

    def set_one(scores):
        return [sum([int(j) for j in i[:2]]) for i in scores]

    def set_one_ind_home(scores):
        scored = list()
        for i in scores:
            scored.append(i[0])
        return scored

    def set_one_ind_away(scores):
        scored = list()
        for i in scores:
            scored.append(i[1])
        return scored

    def set_two(scores):
        return [sum([int(j) for j in i[2:4]]) for i in scores]


    t1_set1 = set_one(get_scores(team1_home + team1_away))
    t2_set1 = set_one(get_scores(team2_home + team2_away))
    t1_set1_home = set_one(get_scores(team1_home))
    t2_set1_away = set_one(get_scores(team2_away))

    t1_set1_scored_home = set_one_ind_home(get_scores(team1_home))
    t1_set1_scored_away = set_one_ind_home(get_scores(team1_away))
    t2_set1_scored_home = set_one_ind_away(get_scores(team2_home))
    t2_set1_scored_away = set_one_ind_away(get_scores(team2_away))

    def bet_string(list):
        part1 = sorted(list)[:5]
        part2 = sorted(list)[-5:]
        return f'{part1}<{round(mean(list), 1)}>{part2}'

    def try_it_over(total1, total2, ind1, ind11, ind2, ind22):

        total_arg1, total_arg2 = 0, 0
        ind_arg1, ind_arg2 = 0, 0
        home_arg, away_arg = 0, 0

        for i in sorted(total1):
            if len(total1)>=38:
                total_arg1 = total1[3]
            elif 26<=len(total1)<=37:
                total_arg1 = total1[2]
            else:
                total_arg1 = total1[1]

        for i in sorted(total2):
            if len(total2) >= 38:
                total_arg2 = total2[3]
            elif 28 <= len(total2) <= 37:
                total_arg2 = total2[2]
            else:
                total_arg2 = total2[1]

        total_bet = round((total_arg1+total_arg2)/2,1)
        t1_min_home = min(ind1)
        t1_min_away = min(ind11)
        t2_min_home = min(ind2)
        t2_min_away = min(ind22)

        print(f'PRESENT POS: {t1_min_home + 25} -> {t2_min_away + 25}')
        print('LOW AVE: ', total_bet)
        print(f'EXTR.MINIMUM: {min([t1_min_home, t1_min_away, t2_min_home, t2_min_away])+25}')

        return f'PRESENT POS: {t1_min_home + 25} -> {t2_min_away + 25}', f'LOW AVE: {total_bet}',\
            f'EXTR.MINIMUM: {min([t1_min_home, t1_min_away, t2_min_home, t2_min_away])+25}'


    bet1, bet2, bet3 = \
        try_it_over(sorted(t1_set1), sorted(t2_set1),
                t1_set1_scored_home, t1_set1_scored_away, t2_set1_scored_home, t2_set1_scored_away)


    current_score = f'{score_one}:{score_two}'


    def bet_string(list):
        part1 = sorted(list)[:5]
        part2 = sorted(list)[-5:]
        return f'{part1}<{round(mean(list), 1)}>{part2}'

    if checker == 1 :
        bet = (title,"TIME :"+str(time),"SCORE: "+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
            "1 SET >>>",
            "1:" + bet_string(t1_set1),
            "2:" + bet_string(t2_set1),
            bet1,
            bet2,
            bet3
                )
        bet_siska(bet)



    print("End of iteration...", checker)
    print()








