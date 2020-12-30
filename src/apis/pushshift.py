# data sources for comment learning
from psaw import PushshiftAPI
from logs.logger import log
import requests
import time


class PS():
  def __init__(self):
    self.api = PushshiftAPI()

  def get_posts(self, subreddit, **kwargs):
    post = self._ps_search(subreddit, **kwargs)
    # log.info(f"post: {post}")
    return post
  
  def get_comments(self, subreddit):
    return self.api.search_comments(q='', subreddit=subreddit)

  def _ps_search(self, subreddit, before=None, after=None, score=None, limit=1):
    cur_time = int(time.time())
    after=(cur_time - 31556952) if after == None else None
    before=(cur_time - 31449600) if before == None else None
    score = 5000 if score == None else None
    url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}"
    url = (url + f"&before={before}") if before else ""
    url = (url + f"&after={after}") if after else ""
    url = (url + f"&score>={score}") if score else ""
    url = (url + f"&limit={limit}") if limit else ""
    log.info(f"pushshift-url: {url}")

    try:
      response = requests.get(url).json().get("data", [])
      return response
    except Exception as e:
      # unable to get data from pushshift
      return None

