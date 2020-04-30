import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://srcsvtqzajbsqa:2816e69dcd518b6d8c414d3104dc153014046967147714f3d525fa2b2ed783ca@ec2-54-86-170-8.compute-1.amazonaws.com:5432/d1f5f7l7rlidba")
db = scoped_session(sessionmaker(bind=engine))


def main():
    count=0
    op=open("books.csv")
    reader=csv.reader(op)
    for i,j,k,l in reader:
        db.execute("INSERT INTO books(isbn,title,author,year) VALUES(:isbn,:title,:author,:year)",{"isbn":i,"title":j,"author":k,"year":l})
        count+=1
        if count == 1000 or count == 2000 or count == 3000 or count == 4000 or count == 5000:
            print("Line {}/5000 inserted".format(count))
    db.commit()

    print("DATA SUCCESSFULLY INSERTED INTO THE DATABASE!")

if __name__ == "__main__":
    main()
