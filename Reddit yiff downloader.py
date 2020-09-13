#%%
import os, praw, time, re, urllib.request, sys
import requests as rq
from tqdm import tqdm
import numpy as np
import threading
import concurrent.futures
from dotenv import load_dotenv

load_dotenv('reddit.env')


start = time.perf_counter()

img_exts= re.compile("\/*.(jpg|jpeg|png|gif)$")
#Save file path for each image uses directory script is in
Save_path = {
    'gfur':f'\\gfur\\',
    'gyiff' : '\\gyiff\\',
    'yiffgif' : '\\yiffgif\\',
    'dragonpenis' : '\\dragonpenis\\',
    'yiff':'\\yiff\\'
}

Limit = int(input("please enter the number of Post to search "))# Note wont download Number of images becaue some post might not be images
#actual_url = int(Limit)

reddit = praw.Reddit(
    client_id=os.getenv('client_id'),
    client_secret =os.getenv('client_secret'),
    user_agent = os.getenv('user_agent')
)



#%%
urls = []

subreddits = [
    'gfur',
    'gyiff',
    'yiffgif',
    'dragonpenis',
    'yiff',
]

#list of submissions per sub reddit
submissions= []

#going to move this back later was here for testing reasons
if not os.path.exists('gfur'):
    os.mkdir('gfur')
    os.mkdir('gyiff')
    os.mkdir('yiffgif')
    os.mkdir('dragonpenis')
urls =[]
workToDo = list()
num_theads = 50

def GrabSubreddit(subredditLists):
    for subreddit in subreddits:
        #subreddit = subredditLists
        submission = list(reddit.subreddit(subreddit).hot(limit = Limit));
        submissions.append(submission)
        #DownloadImages(submissions, subreddit)
def DownloadImages(submissions, path):
    for index, submission in tqdm(enumerate(submissions), total = len(submissions), unit = ' Owo', desc = f"downloading - {path} - ^>^"):
        url = submission.url
        #name = submission.title
        #karma = submission.score
        isMatch = len(img_exts.findall(url)) > 0

        # process = threading.Thread(target=download_gfur)
        if isMatch: #and karma >= 100:
            img_data = rq.get(url, stream = True).content
            imgexts = img_exts
            fExt = img_exts.findall(url)[0]
            root_path = os.path.dirname(sys.argv[0])
            filename = f"{root_path}{Save_path[path]}{path}-{index + 1}.{fExt}"
            with open(filename, 'wb+') as f:
                f.write(img_data)

print('pounces on threads')

def main():
    GrabSubreddit(subreddits)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(DownloadImages, submissions,subreddits)
if __name__ == '__main__':
    main()

finish = time.perf_counter()
print(f'Finished in {round(finish-start,2)} seconds')
# %%
