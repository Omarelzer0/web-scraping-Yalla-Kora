import pandas as pd
import requests
from bs4 import BeautifulSoup

date = input("please enter the date in this format mm/dd/yyyy")
page = requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}")

def main(page):
    # تحويل الصفحة من كود بايت إلى HTML
    src = page.content
    soup = BeautifulSoup(src, "html.parser")
    
    match_details = []

    # البحث عن جميع البطولات
    championships = soup.find_all("div", {'class': 'matchCard'})

    def get_match_info(championship):
        championship_title = championship.find("h2").text.strip()
        all_matches = championship.find("div", {'class': 'ul'}).find_all("div", {'class': 'liItem'})

        for match in all_matches:
            # الحصول على تفاصيل المباراة
            no_of_round = match.find("div", {'class': 'date'}).text.strip()
            team_A = match.find("div", {'class': 'teamA'}).text.strip()
            team_B = match.find("div", {'class': 'teamB'}).text.strip()
            match_info = f"{team_B}  V.S  {team_A}"
            result = match.find("div", {'class': 'MResult'}).find_all("span", {'class': 'score'})
            score = f"{result[0].text.strip()} -  {result[1].text.strip()}"
            match_time = match.find("div", {'class': 'MResult'}).find("span", {'class': 'time'}).text.strip()
            match_status = match.find("div", {'class': 'matchStatus'}).text.strip()

            # إضافة التفاصيل إلى القائمة
            match_details.append({
                "نوع البطوله": championship_title,
                "رقم الجوله ": no_of_round,
                "الفرق": match_info,
                "نتيجه المباراه ": score,
                "توقيت المباراه": match_time,
                "حاله المباراه": match_status
            })

    # استخراج تفاصيل المباريات من البطولات
    for championship in championships:
        get_match_info(championship)

    # تحويل القائمة إلى pandas DataFrame
    df = pd.DataFrame(match_details)

    # تصدير البيانات إلى ملف CSV
    df.to_excel(r'D:\ROAD TO BE DATA SCIENTIST\WEB SCRAPING\1st project\matches_details.xlsx', index=False)
    print("File created successfully")

main(page)
