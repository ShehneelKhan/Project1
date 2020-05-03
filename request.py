import requests

res = requests.get("https://www.goodreads.com/book/title.json", params={"key": "TzAs9qZiNLUZ3xl1cpDzSg" , 'title': "Legend"})
print(res.json())
