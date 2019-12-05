import datetime
import json
import requests
import os

connpass_url = "https://connpass.com/api/v1/event/"
ifttt_url = "https://maker.ifttt.com/trigger/get_connpass_event/with/key/" + os.getenv("IFTTT_API_KEY")
connpass_params = {
    "order": 3,
    "count": 100,
}
dt_now = datetime.datetime.now(
    datetime.timezone(datetime.timedelta(hours=9))
).strftime("%Y-%m-%d")

response = requests.get(connpass_url, connpass_params)
print(response)
data = response.json()

osaka_events = []
for event in data["events"]:
    if event["address"] is not None:
        if "大阪" in event["address"] and event["updated_at"][0: 10] == dt_now:
            osaka_events.append(event)

for osaka_event in osaka_events:
    started_at = datetime.datetime.strptime(osaka_event["started_at"], "%Y-%m-%dT%H:%M:%S+09:00")
    ended_at = datetime.datetime.strptime(osaka_event["ended_at"], "%Y-%m-%dT%H:%M:%S+09:00")
    place = osaka_event["place"]
    title = osaka_event["title"]
    event_url = osaka_event["event_url"]
    hash_tag = osaka_event["hash_tag"]

    if started_at.date() == ended_at.date():
        datetime_text = (
                str(started_at.year) + "年"
                + str(started_at.month) + "月"
                + str(started_at.day) + "日"
                + ["(月)", "(火)", "(水)", "(木)", "(金)", "(土)", "(日)"][started_at.weekday()]
                + str(started_at.hour) + "時"
                + str(started_at.minute)
                + ("0" if started_at.minute==0 else "") + "分" + "~"
                + str(ended_at.hour) + "時"
                + str(ended_at.minute)
                + ("0" if ended_at.minute==0 else "") + "分"
                + "\n"
        )
    else:
        datetime_text = (
                str(started_at.year) + "年"
                + str(started_at.month) + "月"
                + str(started_at.day) + "日"
                + ["(月)", "(火)", "(水)", "(木)", "(金)", "(土)", "(日)"][started_at.weekday()]
                + str(started_at.hour) + "時"
                + str(started_at.minute)
                + ("0" if ended_at.minute==0 else "") + "分" + "~"
                + str(ended_at.year) + "年"
                + str(ended_at.month) + "月"
                + str(ended_at.day) + "日"
                + ["(月)", "(火)", "(水)", "(木)", "(金)", "(土)", "(日)"][started_at.weekday()]
                + str(ended_at.hour) + "時"
                + str(ended_at.minute)
                + ("0" if ended_at.minute==0 else "") + "分"
                + "\n"
        )
    title = title + "\n"
    if place is None:
        place = "開催場所不明\n"
    else:
        place += "\n"
    if hash_tag is "":
        pass
    else:
        hash_tag = "#" + hash_tag + "\n"
    event_url += "\n"
    tweet_text = datetime_text + title + place + hash_tag + event_url
    ifttt_params = {
        'value1': tweet_text,
    }
    print(tweet_text)
    res = requests.post(ifttt_url, ifttt_params)
    print(res)

