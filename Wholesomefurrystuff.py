import os, praw, time, re, urllib.request, sys
import requests as rq
from tqdm import tqdm
import numpy as np
from queue import Queue
import threading 
import concurrent.futures

load_dotenv('reddit.env')


start = time.perf_counter()
urls=[]
img_exts= re.compile("\/*.(jpg|jpeg|png|gif|mp4|wmv)$")
#Save file path for each image uses directory script is in
file_path= 'C:\\Users\\Creat\\Pictures\\wholsomefurrymeme\\'
Save_path = {
    'furry_irl':'\\furry_irl\\',
    'wholesome_furries' : '\\wholesome_furries\\',
 
                           
}

Limit = 5 #int(input("please enter the number of Post to search "))# Note wont download Number of images becaue some post might not be images
#actual_url = int(Limit)

reddit = praw.Reddit(
    client_id=os.getenv('client_id'),
    client_secret =os.getenv('client_secret'),
    user_agent = os.getenv('user_agent')
)

subreddits = [
    'furry_irl'  ,
    'wholesome_furries',
    
]

workToDo = list()
num_theads = 50

def GrabSubreddit(subredditList):
    for subreddit in subreddits:
        if not os.path.exists(f"{ file_path}{subreddit}"): os.mkdir(f"{file_path}{subreddit}")
        submissions = reddit.subreddit(subreddit).hot(limit = Limit)
        DownloadImages(submissions, subreddit)

def DownloadImages(submissions, path):
    for index, submission in tqdm(enumerate(submissions)):
        url = submission.url
        #name = submission.title
        #karma = submission.score              
        isMatch = len(img_exts.findall(url)) > 0
        urls.append(url)
        # process = threading.Thread(target=download_gfur)
        if isMatch: #and karma >= 100:
            img_data = rq.get(url, stream = True).content
            imgexts = img_exts
            fExt = img_exts.findall(url)[0]
            
            root_path = os.path.dirname(file_path)
            filename = f"{root_path}{Save_path[path]}{path}-{index + 1}.{fExt}"
            with open(filename, 'wb+') as f:
                f.write(img_data)


print('pounces on threads')
thread = []
def main():
    GrabSubreddit(subreddits)


if __name__ == '__main__':
    main()

finish = time.perf_counter()
print(f'Finished in {round(finish-start,2)} seconds')