from bs4 import BeautifulSoup
import requests
import pandas as pd
import dateparser



class Twitter:

    def __init__(self):

        self.counter = 1
        self.col_names = ['id', 'p_message', 'tweet_time', 'p_url', 'username']
        self.records = []


    def main(self, username):
        print(username)

        url = f'https://twitter.com/{username}'
        
        #make soup (all post page) ----------------------
        page_soup = self.make_soup(url)
        if not page_soup:
            print('Error in Soup..')
            return

        try:
            all_tweets = page_soup.select('li[class="js-stream-item stream-item stream-item"]')
        except:
            all_tweets = page_soup.select('li[class="js-stream-item stream-item stream-item "]')

        if len (all_tweets)==0:
            all_tweets = page_soup.select('li[class="js-stream-item stream-item stream-item "]')
        
        if not all_tweets:
            print('tweets not found...!')
            return

        self.getting_post_data('no-thread', all_tweets, username) #start here---

        #dump data into postgres ----
        if self.records:
            data = pd.DataFrame(self.records, columns=self.col_names) 
            data = data[['tweet_time', 'p_message']]
            
            return data
    

    def get_description(self, tweet):
        try:
            body = tweet.find('div', 'js-tweet-text-container')
            body_text = str(body)
            
            return BeautifulSoup(body_text, 'html.parser').text
        except:
            print('description not found...!')
            return ''

    def post_data(self, tweet):
        try:
            description = self.get_description(tweet)

            try:
                timestamp = tweet.select_one('[data-time-ms]').get('data-time-ms')
                tweet_time = dateparser.parse(timestamp)
            except: 
                tweet_time = None
                            
            tweet_url = 'https://twitter.com' + tweet.find('a', 'tweet-timestamp js-permalink js-nav js-tooltip').get('href')
            
            return description, tweet_time, tweet_url
        except:
            return 3 * (None,)

    
    def make_soup(self, url):
        try:
            headers = {'User-Agent': 'Google Bot', 'Accept-Language': "en-US,en;q=0.5"}
            page = requests.get(url, headers=headers, timeout=4)

            return BeautifulSoup(page.content, 'html.parser')
        except:
            return None
            

    def getting_post_data(self, thread_name, all_tweets, username):

        for tweet in all_tweets:
            try:
                tweet_id = tweet.get('data-item-id')
                description, tweet_time, tweet_url = self.post_data(tweet)
                
                if not description:
                    continue

                self.records.append((tweet_id, description, tweet_time, tweet_url, username))

                print ('twitter:_____%s_____%d' %(thread_name, self.counter))
                
                self.counter += 1
            except:
                print('something wrong..!')
                continue