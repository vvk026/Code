from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app=Flask(__name__)
@app.route('/',methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')
@app.route('/Times_review',methods=['GET','POST'])
@cross_origin()
def index():
    if request.method=='POST':
        try:
            skill=request.form['content'].replace(" ",",")
            site = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={skill}&txtLocation="
            site_open = uReq(site)
            site_read= site_open.read()
            site_bs=bs(site_read,'lxml')
            site_get= site_bs.find_all('li', {"class": "clearfix job-bx wht-shd-bx"})
            site_get_1 = site_bs.find_all('ul', {"class": "top-jd-dtl clearfix"})
            site_get_2 = site_bs.find_all('ul', {"class": "list-job-dtl clearfix"})
            reviews = []
            with open('jobs.txt','w') as f1:
                for i in range(len(site_get)):
                    l = site_get[i].a['href']
                    company1 = site_get[i].h3.text.strip()
                    job=site_get[i].a.text.strip()
                    location=site_get_1[i].span.text.strip()
                    description=site_get_2[i].li.text.strip().split('\n')[1]
                    skills=site_get_2[i].span.text.strip()
                    a = {'company': company1,"job_title":job,"Location":location,"Description":description,"Skills_req":skills}
                    f1.write(f"company: {company1}")
                    f1.write('\n')
                    f1.write(f"job_title:{job}")
                    f1.write('\n')
                    f1.write(f"Details: {l}")
                    f1.write('\n')
                    f1.write(f"Location: {location}")
                    f1.write('\n')
                    f1.write(f"Description: {description}")
                    f1.write('\n')
                    f1.write(f"Skills_req: {skills}")
                    f1.write('\n')
                    f1.write('\n')

                    reviews.append(a)
                return render_template('results.html', reviews=reviews[0:(len(reviews) - 1)])
        except Exception as e:
            print(e)
    else:
        return render_template('index.html')



if __name__ == "__main__":
    app.run()

