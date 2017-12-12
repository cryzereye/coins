rates notification for Bitcoin trading using Coins.ph

COINS v1 (legacy)
How to use v1:
1. Run start.bat
2. Input B if you bought BTC in your last transaction, and S if you sold BTC on your most recent transaction
3. Enter the rate used in your last transaction
4. When you did a transaction, press ~ (SHIFT + \`) to update inputs

-----------------------------------
            COINS v2
-----------------------------------
How to use:
1. Run run_v2.bat
2. If you did not do any transaction between now and your last use of v2, you can just enter Y when asked about the profile. Else, kindly enter the following:
    - Last action done,
    - Rate used in last transaction
    - Remaining money
    - Remaining BTC
3. Profile entered above will be saved to profile.json. This can be reused on your discretion.
4. When you did a transaction, press ~ (SHIFT + \`) to update inputs

Columns:
1. BUY - shows current buy rate
2. SELL - shows current sell rate
3. RATE - shows your last rate used
4. PROFIT - shows your profit based on your last money/btc amount if you buy/sell using latest rates
5. DO - action to do that will profit you
6. DELTA - shows change in rates
         - 1 + means rates increased by below 1999 php, 1000 per + if multiple
         - 1 - means rates decreased by below 1999 php, 1000 per + if multiple


NOTE:
- This is "optimized" for full buy/sell transactions. v2 can be used for partial buy/sell. Just reset your profile
- After the rates are shown, you have ~30 seconds to do your action

donate:  3B2bVeQJ2424v5tALhpaaeNzc42RYTRdMF 
