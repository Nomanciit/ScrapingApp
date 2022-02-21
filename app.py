import streamlit as st
import twint
import pandas as pd
from functions import get_csv_download_link
from twitter_crawler import Twitter
twitter_crawler = Twitter()

from k_extraction import KeyPhrases 
k = KeyPhrases()
# Set page name and favicon
st.set_page_config(page_title='Twitter scraper',page_icon=':iphone:')



st.image('dark_banner.png')
st.subheader("""
Let's scrape some Tweets... Hope Twitter doesn't ban me :smile:
""")

# customize form
with st.form(key='Twitter_form'):
    search_term = st.text_input('What do you want to search for?')
    limit = st.slider('How many tweets do you want to get?', 0, 500, step=5)
    output_csv = st.radio('Save a CSV file?', ['Yes', 'No'])
    file_name = st.text_input('Name the CSV file:')
    submit_button = st.form_submit_button(label='Search')

    if submit_button:
      username = search_term
      data = twitter_crawler.main(username)
      data['keywords'] = data['p_message'].apply(k.keyword_extraction)
      # data = pd.read_csv(f'{file_name}.csv')
      st.table(data)

#         if output_csv == 'Yes':
#             st.markdown(get_csv_download_link(data, file_name), unsafe_allow_html=True)

