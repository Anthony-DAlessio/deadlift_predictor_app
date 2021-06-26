import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## About the Raw Deadlift Predictor

            This simple tool exists to aid a decisionmaking process I (and virtually anyone involved in barbell sport for any meaningful length of time) engage in all the time. 
            A great deal has been written on the topic of training economy and how it might be optimized, and by people much more competent than I am. However, I think all
            of that can be of only so much use to someone who doesn't appreciate the problems he has to begin with; without the benefit of experience or the advice of a knowledgeable
            third party it is very easy to apply correct solutions to nonexistent problems, going nowhere. While this predictor is no substitute for more specific knowlege and 
            experience, I hope it might nevertheless help someone avoid wasting time as I've done. What follows is a description of how it was made and how it works. 


            """
        ),
        dcc.Markdown(
            """
            ## Exploratory Data Analysis

            The dataset used to build these models is a snapshot of the Open Powerlifting meet results database, which comprises 1.4 million or so (and counting) observations, and each of those in turn 
            being made up of 37 metrics. Since my project is fairly specific in scope (our target is the deadlift only), it was immediately clear that the majority of the data here was 
            not relevant; wrangling it into something more manageable is where the bulk of the time spent on the project went. For context, the original features of the data were the 
            following:

            """
        ),
        dcc.Markdown(
            """
            'Name'- The lifter's name
            'Sex'- The lifter's sex 
            'Event'- The event the lifter competed in (in this context, full meet versus single lift)
            'Equipment'- The equipment category the lifter competed in (ranging from raw to multi-ply)
            'Age'-The lifter's age
            'AgeClass'-The lifter's age class
            'Division'-The group against whom a lifter is competing, often delineated by age class
            'BodyweightKg'-The lifter's weight in kg
            'WeightClassKg'-The lifter's weight class
            'Squat1Kg', 'Squat2Kg', 'Squat3Kg','Squat4Kg'-The lifter's first, second, third and (if applicable) fourth squat attempt results
            'Best3SquatKg'-The best of the lifter's normal 3 attempts, used to calculate total 
            'Bench1Kg', 'Bench2Kg', 'Bench3Kg','Bench4Kg', 'Best3BenchKg'-The same as the above, but for the bench press
            'Deadlift1Kg', 'Deadlift2Kg', 'Deadlift3Kg','Deadlift4Kg'-The deadlift attempt results 
            'Best3DeadliftKg'-The best of the normal 3 deadlift attempts, used to calculate total. This is our target. 
            'TotalKg'-The lifter's competition total
            'Place'-Where the lifter placed in his division and weight class 
            'Wilks'-A coefficient used to compare performance across categories. We'll go over this in more detail below.
            'McCulloch', 'Glossbrenner', 'IPFPoints'-More derived values meant to serve a similar function to Wilks as a universal comparitor  
            'Tested'-Whether or not the lifter was drug tested
            'Country'-The lifter's country 
            'Federation', 'Date', 'MeetCountry', 'MeetState', 'MeetName'- The federation, date, country, state (if applicable), and name of the meet where the observation took place

            """, dedent=False

        ),
        dcc.Markdown(
            """
            Looking through the data it was clear that the observations were both very numerous and diverse in ways that probably wouldn't contribute to the predictive accuracy of 
            my modeling. Since I was focused on only the deadlift I was able to take steps to both limit the scope of the data to something more manageable and increase accuracy by eliminating 
            confounding variables, focusing on features of interest in comparitively homogenous subsets of the data. Specifically:

            """
        ),
            dcc.Markdown(
            """
            1. Split the data by sex. Modeling males and females separately avoids well rehearsed sex differences obscuring the effect of more useful variables. 
            2. Eliminate equipped categories. The nuances introduced by single and multiply gear are not my concern here. 
            3. Eliminate events other than full competition. Training for bench press only competition and the like may be interesting, but it's just a distraction here. 
            4. Eliminate observations that "placed" as disqualified (DQ). The most common way to be disqualified from a meet is to "bomb out," or fail to produce a successful attempt on one of the lifts. Getting rid of these here is both more accurate and less trouble than trying to impute them later.
            5. Eliminate observations with Wilks scores below 150. This is an outlier reduction/quality control decision. 

            """, dedent=False
        ),
            dcc.Markdown(
            """
            With the number of observations groomed into a more manageable state in the tens of thousands, I could proceed to eliminate features that weren't useful. 
            These fell into 3 basic categories: 

            """
        ),
        dcc.Markdown(
            """
            Irrelevant: Name, Date, Place, Tested, Country, Federation, MeetCountry, MeetState, and Meetname
            Redundant: Sex, Event, Equipment, Division (as a result of the above cleaning) as well as the attempt specific features (made redundant by the "Best" features)
            Leaky: Totalkg, Wilks, McCulloch, Glossbrenner, and IPFPoints

            """, dedent=False
        ),
        dcc.Markdown(
            """
            It's worth spending just a bit of time on the Wilks score (both to see why it and similar metrics are leaky and to understand what I'm doing with it later).
            Comparing performance across weight classes fairly has historically been tricky business; absolute weight lifted is obviously unfair in favor of heavy weight classes,
            and weight lifted:bodyweight ratio is similarly biased in favor of light weight classes. Wilks score is an attempt (with relatively widespread acceptance) to solve this 
            by multiplying total lifted by a coefficient that scales with bodyweight, with the formula below. 

            """
        ),
        
        html.Img(src='assets/wilkscrop.jpg'),

        dcc.Markdown(
            """
            The problem for us, unfortunately, is that a metric like this (or the others above that function similarly) represents data leakage that would
            reduce our "predictions" to trivial algebra. We don't have to throw it away completely, however; because Wilks score scales with total lifted (irrespective of where
            those kilos come from) we can partly preserve it by doing a little feature engineering.

            """
        ),
        dcc.Markdown(
            """
            ## Feature Engineering

            We can restore some of the information to our dataset by calculating the contribution of the other lifts to a lifter's Wilks sans deadlift, and possibly add more
            by doing so for each lift individually (which allows their relative contributions to be compared). These "[lift] Wilks" features are simply Wilks scores with
            individual lifts instead of totals. The coefficients are unchanged. (The features for males are shown below, but those for females are identical but for the coefficients)

            """
        ),
        dcc.Markdown(
            """``
            
            a = -216.0475144
            b = 16.2606339
            c = -0.002388645
            d = -0.00113732
            e = 0.00000701863
            f = -0.00000001291

            df['Squat Wilks'] = df['Best3SquatKg'] * 500 /(a+(b*df['BodyweightKg'])+(c*df['BodyweightKg']**2)+(d*df['BodyweightKg']**3)+(e*df['BodyweightKg']**4)+(f*df['BodyweightKg']**5)) 
            df['Bench Wilks'] = df['Best3BenchKg'] * 500 /(a+(b*df['BodyweightKg'])+(c*df['BodyweightKg']**2)+(d*df['BodyweightKg']**3)+(e*df['BodyweightKg']**4)+(f*df['BodyweightKg']**5)) 
            """
            
        ),
        dcc.Markdown(
            """
            In addition to Wilks features, I thought I might try to use this opportunity to test some folk wisdom that exists germane to this topic. A nontrivial part of the 
            difference between lifters' relative lift perfomance is often said to be a result of differing anthropometry; specifically, different limb lengths and the resulting leverages.
            Long arms are supposed to be favorable for the deadlift and a liability in the bench press, and short arms the reverse. While there isn't any direct anthropometric data 
            in this dataset, I tried to approximate some by making a couple of assumptions. First, that people with longer arms tend to be heavier (purely as a result of a 
            larger frame in general), and second that people with shorter arms (if they indeed enjoy an advantage in the bench press) are likely to have a larger bench press relative
            to their other lifts (including the squat, which remains a feature in our data). These assumptions give us a feature apiece. 

            """
        ),
        dcc.Markdown(
            """``
            
            df['Bench:Bodyweight Ratio'] = df['Best3BenchKg']/df['BodyweightKg']
            df['Bench:Squat Ratio'] = df['Best3BenchKg']/df['Best3SquatKg']
            
            """
            
        ),
        dcc.Markdown(
            """
            This brings us down from 1.4 million observations and 37 features of noise to pre-split sets of about 50,000 observations and 10 features. Their individual relationships
            to the target are charted below.  

            """
        ),
        html.Img(src='assets/age.jpg'),
        html.Img(src='assets/ageclass.jpg'),
        html.Img(src='assets/bodyweight.jpg'),
        html.Img(src='assets/weightclass.jpg'),
        html.Img(src='assets/squat.jpg'),
        html.Img(src='assets/bench.jpg'),
        html.Img(src='assets/swilks.jpg'),
        html.Img(src='assets/bwilks.jpg'),
        html.Img(src='assets/bbratio.jpg'),
        html.Img(src='assets/bsratio.jpg'),

        dcc.Markdown(
            """
            ## Modeling

            With this done I could make some baseline predictions. Given that this is a regression problem the mean seemed like a good starting point. Because males and females
            are modeled separately I decided to use both mean absolute error and mean percentage absolute error as metrics; MAE is meaningful for comparison of performance within
            a given sex category, and MAPE prevents the smaller magnitudes at play in the female models from masquerading as improved performance. The mean, baseline MAE and MAPE
            for males and females were (234.27993213928136, 34.26645791562823, 0.16097736992431438) and (137.93416160770357, 21.525496023199924, 0.16638048152004975) respectively. 
            After a random train/val/test split I trained 2 models for each group; an sklearn linear regression model, and an XGBoost gradient boosting regressor model. After
            tuning them with the validation sets I was able to get final MAE and MAPE on the test sets of (16.57529365957547, 0.0833290359229802) and 
            (16.405122850259605, 0.08228450317249836) for the male linear regression and gradient boosting models respectively, an improvement over baseline of nearly 50%. The
            corresponding metrics for the female models are (10.90783953028571, 0.08231215612011458) and (15.191544535743668, 0.12037356609316421). The permutation importances of 
            these models are below. 


            """
        ),
        html.Img(src='assets/mpimportances.jpg'),
        html.Img(src='assets/fpimportances.jpg'),
        dcc.Markdown(
            """
            ## Interpretation

            While we've achieved good accuracy and handily beaten the baseline, our little experiment in anthropometry yielded decidedly mixed results. Comparison between the two 
            types of model is a bit awkward because of how enormously important the squat is in gradient boosting ones, but it still seems clear that while there might be something
            to the bench:bodyweight ratio (particularly in light of the fact that a lot of the remaining explanatory real estate is occupied by bench wilks, the other feature relating
            bench to bodyweight), bench:squat ratio doesn't seem to mean much. Maybe it wasn't a good proxy for short arms, or short arms aren't as advantageous in the bench press
            as people think. Alternatively, people with short arms might also tend to have short legs, and be gaining a benefit in the squat to match. Without more direct analysis it's
            hard to say.  

            On a final note regarding what we can say and what we can't, it's worth bearing in mind who this tool is (and isn't) for. I've tried to make it clear at the outset from 
            the name, but these models are for raw lifters. The exclusions made at the EDA stage were substantial, and the differences between raw and equipped (particularly multi-ply)
            lifts are too. It might be an interesting exercise to repeat these steps for geared lifters, but it's one I leave to an equipped student of data science for now. 

            Having addressed the people who aren't raw lifters because they aren't raw, we're left to address the ones who aren't lifters. The exclusion of observations with Wilks 
            scores below 150 was because they were strange outliers, but they were strange outliers because at the level of performance adaptation (or lack thereof) represented by a 
            150 Wilks, none of these things are likely to matter at all. Such a person's lifts are more likely to be a function of what they do for a living or leisure more than
            anything else. 


            """
        ),
        




        
    ],
    md=12,
)

column2 = dbc.Col([])

layout = dbc.Row([column1])