import candles
import divergences

# Global
import json
import warnings
warnings.filterwarnings('ignore')

# Divergences ---------------------------

def get_df(token):
    df = candles.get_hourly(token)
    df_daily = candles.get_daily(token)
    df_weekly = candles.resample_data(df_daily, '1','WEEK')
    df_weekly = df_weekly.reset_index(level=None, drop=False, inplace=False, col_level=0)
    return df, df_weekly

def get_signals(tokens, durations):
    signals =[]
    for token in tokens:
        print(token)
        try:
            df, df_weekly = get_df(token)
            for duration in durations:
                try:
                    duration_split = duration.split()
                    df_new = candles.resample_data(df, duration_split[0], duration_split[1])
                    df_new = df_new.reset_index(level=None, drop=False, inplace=False, col_level=0)
                    div_df = divergences.find_divergence(df_new, df_weekly, duration_split[0])
                    if (div_df is not None):
                        dict_div = {}
                        dict_div['token']        = token
                        dict_div['duration']     = duration
                        dict_div['start']        = div_df['start'].strftime("%Y-%m-%d %H:%M")
                        dict_div['end']          = div_df['end'].strftime("%Y-%m-%d %H:%M")
                        dict_div['type']         = div_df['type']
                        dict_div['cosine']       = round(div_df['cosine'], 3)
                        dict_div['market_state'] = div_df['market_state']
                        dict_div['volatility']   = div_df['volatility']
                        signals.append(dict_div)
                except Exception as e:
                    print(e)
                    print('Skipping '+str(token)+' on '+str(duration))
        except Exception as e:
            print(e)
            print('Skipping '+str(token))

    return(signals)

def post_signals():
    tokens = ['BTC', 'ETH', 'XRP', 'LTC', 'BAB', 'BCH', 'EOS', 
              'BAT', 'XLM', 'BNB', 'ADA', 'BSV', 'TRX', 'XTZ', 
              'ATOM', 'ETC', 'NEO', 'XEM', 'MKR', 'ONT', 'LINK', 
              'ZEC', 'VET', 'CRO', 'DOGE', 'QTUM', 'OMG', 'DCR', 
              'HOT', 'WAVES', 'BTT','TUSD', 'LSK', 'NANO', 'REP',
              'BCD', 'RVN', 'ZIL', 'ZRX', 'ICX','XVG', 'PAX', 
              'BTS', 'BCN', 'DGB', 'NPXS', 'HT', 'IOST', 'AE', 
              'KMD', 'ABBD', 'SC', 'ENJ', 'STEEM', 'AOA', 'QBIT', 
              'BTM','MAID', 'THR', 'SOLVE', 'INB', 'KCS','THETA', 
              'WTC', 'STRAT', 'SNT', 'CNX', 'DENT', 'GNT', 'MCO', 
              'ELF', 'DAI', 'ARDR', 'FCT', 'XIN', 'VEST', 'TRUE', 
              'ZEN', 'SAN', 'PAI', 'ARK','MONA', 'DGD', 'GXC', 'WAX',
              'CLAM', 'AION', 'LRC', 'MATIC', 'MANA', 'ELA', 'LOOM',
              'PPT', 'NET']

    tokens = tokens[:20] # Top 20
    durations = ['2 HOUR','4 HOUR','8 HOUR','12 HOUR']
    signals = get_signals(tokens, durations)
    
    print(signals)


post_signals()