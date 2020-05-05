import requests

res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "TzAs9qZiNLUZ3xl1cpDzSg" , 'isbns': "345379063"})
print(res.json())
