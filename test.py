from scan import current_moment,get_link,handling
from parsing import check_link
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
from send import errormsg,made_mistake
from send import bet_siska

options = webdriver.ChromeOptions()
options.add_argument('--mute-audio')
browser = webdriver.Chrome(options=options)
browser.get("https://www.volleyball24.com/")
switch_to_live = browser.find_element(By.CSS_SELECTOR, "div.filters__tab:nth-child(2) > div:nth-child(2)")
switch_to_live.click()
sleep(1)

scanset1 = set()
scanset2 = set()


def try_it(score1, score2):
    if abs(score1 - score2) >= 7 and score1 <23 and score2 < 23:
        return True

while True:
    try:
        matches = browser.find_elements(By.CSS_SELECTOR,"[id^='g_12']")
        for i in matches:
            try:

                time,score_one,score_two,score_line = handling(i)
                set = current_moment(time)
                t1_set1 = score_line[0]
                t2_set1 = score_line[1]
                t1_set2 = score_line[2]
                t2_set2 = score_line[3]


                if set == 1 and try_it(t1_set1, t2_set1) == True:
                    link = get_link(i)
                    checker = 1
                    if link in scanset1:
                        continue
                    scanset1.add(link)
                    check_link(link, set, t1_set1, t2_set1, checker, score_line)


            except Exception as fail:
                print('Mistake level 1')
                print(fail)
                sleep(2)
                continue

    except Exception as fail:
        print('Mistake level 2')
        print(fail)
        sleep(2)
        continue
    sleep(15)