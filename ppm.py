import requests
import tweepy 
import pandas as pd

def ppmbot():
    # Consumer keys and access tokens, used for Tweepy
    CONSUMER_KEY = <<Get your key from the Twitter Dev website>>
    CONSUMER_SECRET = <<Get your key from the Twitter Dev website>>
    ACCESS_KEY = <<Get your key from the Twitter Dev website>>
    ACCESS_SECRET = <<Get your key from the Twitter Dev website>>
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    
    #Accessing the Fantasy Premier League API
    element_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    req = requests.get(element_url)
    fpl_data = req.json()
    
    #Get the total points
    elements_df = pd.DataFrame(fpl_data['elements'])
    elements_df = elements_df[['web_name','now_cost','total_points']]
    elements_df['now_cost'] = elements_df['now_cost'] / 10
    
    #Calculate PPM
    elements_df['PPM'] = elements_df['total_points'] / elements_df['now_cost']
    
    #Get Top 5 PPM
    ppm_df = elements_df.sort_values('PPM', ascending=False).head(5)
    
    #Create Your Tweet
    ppm_list = []
    for i,r in ppm_df.iterrows():
        name = ppm_df.at[i,'web_name']
        ppm_value = round(ppm_df.at[i,'PPM'],2)
        ppm_string = name + ' -' + str(ppm_value)
        ppm_list.append(ppm_string)

    if len(ppm_list):
        ppm_join_sting = "\n".join(ppm_list)
        ppm_final_string = 'Top 5 PPM -\n\n' + ppm_join_sting + '\n\n#FPL #FPLCommunity'
        api.update_status(ppm_final_string)

if __name__ == '__main__':
    ppmbot() 
