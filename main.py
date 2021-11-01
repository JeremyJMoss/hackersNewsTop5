from bs4 import BeautifulSoup
import requests
from smtplib import SMTP
import os

my_email = os.getenv("MY_EMAIL")
password = os.getenv("PASSWORD")

response = requests.get("https://news.ycombinator.com/news")

yc_webpage = response.text

soup = BeautifulSoup(yc_webpage, "html.parser")

articles = soup.find_all(name="a", class_="titlelink")
article_texts = []
article_links = []
article_upvote_scores = []
top_5 = {
    "title": [],
    "link": []
}
for article_tag in articles:
    text = article_tag.get_text()
    link = article_tag.get("href")
    article_texts.append(text)
    article_links.append(link)
article_upvote_list = soup.find_all(class_="score")
for upvote in article_upvote_list:
    article_upvote_scores.append(int(upvote.get_text().split(" ")[0]))

sorted_votes = sorted(article_upvote_scores, reverse=True)
for num in range(0, 5):
    if "https" not in article_links[article_upvote_scores.index(sorted_votes[num])]:
        link = "https://news.ycombinator.com/" + article_links[article_upvote_scores.index(sorted_votes[num])]
        top_5["link"].append(link)
    else:
        top_5["link"].append(article_links[article_upvote_scores.index(sorted_votes[num])])
    top_5["title"].append(article_texts[article_upvote_scores.index(sorted_votes[num])])

message = "Top 5 Hacker News\n\n"
for num in range(0, 5):

    message += f"{num + 1}. {top_5['title'][num]}\n"
    message += f"{top_5['link'][num]}\n\n"


with SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs=os.getenv("TO_EMAIL"),
        msg=f"Subject:Hacker News Top 5 Highest Voted Stories\n\n{message}"
    )


