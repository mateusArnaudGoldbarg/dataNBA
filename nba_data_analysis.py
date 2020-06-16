import pandas as pd #Data manipulativo Library
import numpy as np
import matplotlib.pyplot as plt #Plotting with low level methods
import matplotlib.patches as mpatches #Plotting with low level methods
import seaborn as sns #Plotting with low level methods
import random
import math

def league_analisys_3_points(league_name):
    """
    check the 3 points shots over year
    :param league_name:
    :return:
    """
    #create a new dataframe filtered by the name of the league
    league = teams[teams.lgID == league_name]
    #select just information about 3 points
    league_by_year = league[["o_3pm","o_3pa", "year"]].groupby("year").mean().reset_index()
    #plot 3 made
    sns.regplot(x="year", y="o_3pm", data=league_by_year, color='blue')
    #plot 3 attempted
    sns.regplot(x="year", y="o_3pa", data=league_by_year, color='red')
    plt.ylim(0,1600)
    #attempted color
    red = mpatches.Patch(color='red', label='Attempted')
    #made colot
    blue = mpatches.Patch(color='blue', label='Made')
    plt.legend(handles=[red, blue])
    #Y label
    plt.ylabel('Three Points')
    #Title
    plt.title('Media 3 points by year {}'.format(league_name))
    plt.show()


abbrev = pd.read_csv(r"basketball_abbrev.csv",low_memory=False)
awards_coach = pd.read_csv(r"basketball_awards_coaches.csv",low_memory=False)
awards_player = pd.read_csv(r"basketball_awards_players.csv",low_memory=False)
coaches = pd.read_csv(r"basketball_coaches.csv",low_memory=False)
draft = pd.read_csv(r"basketball_draft.csv",low_memory=False)
hof = pd.read_csv(r"basketball_hof.csv",low_memory=False)
master = pd.read_csv(r"basketball_master.csv",low_memory=False)
all_star = pd.read_csv(r"basketball_player_allstar.csv",low_memory=False)

#Load data
players = pd.read_csv(r"basketball_players.csv",low_memory=False)

series_post = pd.read_csv(r"basketball_series_post.csv",low_memory=False)
teams = pd.read_csv(r"basketball_teams.csv",low_memory=False)

#print(len(players.GP))
#remove all players with Games Played = 0
players.drop(players[players.GP == 0].index,inplace=True)
#print(len(players.GP))

points_max = players.points.max()
playerMax = players.points.idxmax()

#PART 1
#=======================================================1.1===================================================
#check the mean
points_mean = players.points.mean()
#check the median
points_median = players.points.median()
print("Points: Mean {}, Median {}".format(points_mean,points_median))

#=======================================================1.2===================================================
#print the highest scorer
print(players[["playerID","points","year","tmID"]].sort_values("points",ascending = False).head(1))

#=======================================================1.3===================================================

#boxplot
sns.boxplot(data=players[['points','rebounds','assists']])
#show figure
plt.show()

#=======================================================1.4===================================================
#Median of points by year
sns.lineplot(x="year", y = "points",data = players,estimator = np.median)
plt.show()


#===========================================================================================================


# PART 2
#=======================================================2.1===================================================

#new data frame
df = players[["playerID","points","fgAttempted","fgMade"]].sort_values("points",ascending = False)[0:22]
#new column to data frame
df['efficiency(%)'] = (df.fgMade/df.fgAttempted)*100
print(df)

#Bar plot of field goal attempted
sns.barplot(x="playerID", y = "fgAttempted",data = df,color="red")
#Bar plot of field goal made
sns.barplot(x="playerID", y = "fgMade",data = df,color="blue")
#Title
plt.title("Field Goal")
#Y label
plt.ylabel("Made x Attempted")
#Colors description in legend
red = mpatches.Patch(color='red',label ='Attempted')
blue = mpatches.Patch(color='blue',label ='Made')
plt.legend(handles=[red,blue])
#Range of Axis Y
plt.ylim(0,3200)
plt.show()

#Bar plot
ax1 = sns.barplot(x="playerID", y ="efficiency(%)", data = df)
#title
plt.title("Efficiency")
#Y label
plt.ylabel("%")
plt.show()




#=======================================================2.2===================================================

# Set data
print(players.columns)
#players = pd.read_csv(r"basketball_players.csv",low_memory=False)
#Create new data frame with infomations with the mean
asd = players[['playerID','points','assists','dRebounds','oRebounds','steals','blocks',"fgMade","fgAttempted","threeMade","threeAttempted","ftMade","ftAttempted"]].groupby('playerID').mean().reset_index()
#sort the best 10 in points
asd = asd.sort_values(["points"],ascending = False)[0:4]

#Organize the index
asd.reset_index(drop=True,inplace=True)
#New dataframe to offensive analyses
df = asd[['playerID','points','oRebounds','fgMade','assists']]
df3 = asd[['playerID','steals','dRebounds','blocks']]

#df.groupby(["steals"]).mean().reset_index()
print(df)


df2 = asd[['playerID']]
df2['FieldGoal'] = asd.fgMade/asd.fgAttempted*100
df2['ThreePoints'] = asd.threeMade/asd.threeAttempted*100
df2['FreeThrow'] = asd.ftMade/asd.ftAttempted*100
df2['ThreePoints'] = df2['ThreePoints'].fillna(0)
#print(df2)
#df['three(%)'] = asd['threeMade']/asd['threeAttempted'] * 100
#df['Field Goals(%)'] = asd["fgMade"]/asd["fgAttempted"] * 100




# ------- PART 1: Create background

# number of variable
print(df3)
for i in range(0,len(df.playerID)):
    categories = list(df)[1:]
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([300,600,900,1200,1500,1800,2100], ["300","600","900","1200","1500","1800","2100"], color="grey", size=7)
    plt.ylim(0, 2400)

    # ------- PART 2: Add plots

    # Plot each individual = each line of the data
    # I don't do a loop, because plotting more than 3 groups makes the chart unreadable

    # Ind1

    values = df.loc[i].drop('playerID').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="group A")
    ax.fill(angles, values, 'b', alpha=0.1)
    #plt.legend(df.playerID[i],loc='upper right', bbox_to_anchor=(0.1, 0.1))
    blue = mpatches.Patch(color='blue', label=df.playerID[i])
    plt.legend(handles=[blue])


    plt.show()


# Add legend
#

for i in range(0,len(df2.playerID)):
    categories = list(df2)[1:]
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([25,50,75], ["25%","50%","75%"], color="grey", size=7)
    plt.ylim(0, 100)


    values = df2.loc[i].drop('playerID').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="group A")
    ax.fill(angles, values, 'b', alpha=0.1)

    red = mpatches.Patch(color='blue', label=df2.playerID[i])
    plt.legend(handles=[red])
    plt.show()


for i in range(0,len(df3.playerID)):
    categories = list(df3)[1:]
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([150,300,450,600], ["150","300","450",'600'], color="grey", size=7)
    plt.ylim(0, 600)


    values = df3.loc[i].drop('playerID').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="group A")
    ax.fill(angles, values, 'b', alpha=0.1)

    red = mpatches.Patch(color='blue', label=df3.playerID[i])
    plt.legend(handles=[red])
    plt.show()


#=======================================================2.3===================================================

#New dataframe with infromation abour three shots
players_3 = players[["threeMade","threeAttempted","year"]].groupby("year").mean().reset_index()
#plot shots Made
sns.regplot(x="year", y ="threeMade", data = players_3,color = 'blue')
#plot shots Attempted
sns.regplot(x="year", y ="threeAttempted", data = players_3,color='red')
plt.ylim(0,100)
#label attempted color
red = mpatches.Patch(color='red',label ='Attempted')
#label Made color
blue = mpatches.Patch(color='blue',label ='Made')
#Legend
plt.legend(handles=[red,blue])
#Label Y
plt.ylabel('Three Points')
#Title
plt.title('Media 3 points by year')
plt.show()


players_3['efficiency'] = players_3.threeMade/players_3.threeAttempted * 100
players_3['efficiency'] = players_3['efficiency'].fillna(0)


#BY LEAGUE
teams = pd.read_csv(r"basketball_teams.csv",low_memory=False)
league_analisys_3_points("NBA")
league_analisys_3_points("ABA")
league_analisys_3_points("ABL1")
league_analisys_3_points("NBL")
league_analisys_3_points("NPBL")
league_analisys_3_points("PBLA")



#BY TEAM OF NBA
#create a new dataframe to don't change the original one
team = teams
#remove all leagues diffrent than NBA
team.drop(team[team.lgID != "NBA"].index,inplace=True)
#remove all teams or datas before 1979
team.drop(team[team.year < 1979].index,inplace=True)
#Take just the three points information
team_info = teams[["o_3pm","o_3pa", "year","tmID"]].groupby(["tmID","year"]).mean().reset_index()
#group by the name of the team
lista = team_info[["year","tmID"]].groupby("tmID").mean().reset_index()
#create a list of with the name of each team
a = lista.tmID.to_list()
print(len(a))
for times in a:
    #group by team and by year
    team_info = teams[["o_3pm", "o_3pa", "year", "tmID"]].groupby(["tmID", "year"]).mean().reset_index()
    #select just the jeam in list times
    team_info.drop(team_info[team_info.tmID != times].index, inplace=True)
    #reg plot
    sns.regplot(x="year", y="o_3pm", data=team_info)
    #title
    plt.title("Three points by team and by year")
    plt.show()


#=======================================================3.1===================================================

#GOAT
goat_df= players[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade","GP"]]
#goat_df.columns = [["playerID","points/game","rebounds/game","assists/game","steals/game","blocks/game","fgMade/game","threeMade/game","GP"]]
goat_df['points'] = goat_df['points']/goat_df['GP']
goat_df['rebounds'] = goat_df['rebounds']/goat_df['GP']
goat_df['assists'] = goat_df['assists']/goat_df['GP']
goat_df['steals'] = goat_df['steals']/goat_df['GP']
goat_df['blocks'] = goat_df['blocks']/goat_df['GP']
goat_df['fgMade'] = goat_df['fgMade']/goat_df['GP']
goat_df['threeMade'] = goat_df['threeMade']/goat_df['GP']
#print(goat_df)

print("points")
goatsPoints = goat_df[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].sort_values(["points","rebounds"],ascending=False)[0:21]
goatsP = goatsPoints[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].groupby("playerID").median().reset_index()
goatsP = goatsP[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].sort_values(["points"],ascending=False).reset_index()
print(goatsP)

goat_score = goatsP
goat_score['score'] = 10 - goat_score.index.values
print(goat_score)

print("\nrebounds")
goatsRebounds = goat_df[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].sort_values(["rebounds"],ascending=False)[0:10]
goatsR = goatsPoints[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].groupby("playerID").median().reset_index()
goatsR = goatsR[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].sort_values(["rebounds"],ascending=False).reset_index()
#print(goatsR)

goat_rebounds = goatsR
goat_rebounds['score'] = 10 - goat_rebounds.index.values
#print(goat_rebounds)
goat_score = goat_score.append(goat_rebounds)


print("\nassists")
goatsAssists = goat_df[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].sort_values(["assists"],ascending=False)[0:10]
goatsA = goatsPoints[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].groupby("playerID").median().reset_index()
goatsA = goatsA[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].sort_values(["assists"],ascending=False).reset_index()
#print(goatsA)

goat_assists = goatsA
goat_assists['score'] = 10 - goat_assists.index.values
#print(goat_rebounds)
goat_score = goat_score.append(goat_assists)

print("\nsteals")
goatsSteals = goat_df[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].sort_values(["steals"],ascending=False)[0:10]
goatsS = goatsPoints[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].groupby("playerID").median().reset_index()
goatsS = goatsS[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].sort_values(["assists"],ascending=False).reset_index()
#print(goatsS)

goat_steals = goatsS
goat_steals['score'] = 10 - goat_steals.index.values
#print(goat_rebounds)
goat_score = goat_score.append(goat_steals)

print("\nblocks")
goatsBlocks = goat_df[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].sort_values(["blocks"],ascending=False)[0:10]
goatsB = goatsPoints[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].groupby("playerID").median().reset_index()
goatsB = goatsB[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].sort_values(["blocks"],ascending=False).reset_index()
#print(goatsB)

goat_blocks = goatsB
goat_blocks['score'] = 10 - goat_blocks.index.values
#print(goat_B)
goat_score = goat_score.append(goat_blocks)

print("\nfgMade")
goatsFgMade = goat_df[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].sort_values(["fgMade"],ascending=False)[0:10]
goatsFG = goatsPoints[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].groupby("playerID").median().reset_index()
goatsFG = goatsFG[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].sort_values(["fgMade"],ascending=False).reset_index()
#print(goatsFG)

goat_FG = goatsFG
goat_FG['score'] = 10 - goat_FG.index.values
#print(goat_FG)
goat_score = goat_score.append(goat_FG)

print("\nThree Made")
goatsTMade = goat_df[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].sort_values(["threeMade"],ascending=False)[0:10]
goatsT = goatsPoints[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].groupby("playerID").median().reset_index()
goatsT = goatsT[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]].sort_values(["threeMade"],ascending=False).reset_index()
#print(goatsT)

goat_T = goatsT
goat_T['score'] = 10 - goat_T.index.values
#print(goat_T)
goat_score = goat_score.append(goat_T).reset_index()
#pd.set_option('display.max_columns', None)
print(goat_score)
goat_score_last = goat_score[['playerID','score']].groupby(["playerID"]).sum()
goat_score_last.score = goat_score_last.score/7

goat_score_last = goat_score_last.sort_values(["score"],ascending = False).reset_index()
print(goat_score_last)


#Radar Plot
GOAT = goat_score_last.playerID[0]
GOAT2 = goat_score_last.playerID[1]
GOAT3 = goat_score_last.playerID[2]
print(GOAT)
# Set data

df = goat_score[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]]
#print(df)

# ------- PART 1: Create background

# number of variable
goat_score = players[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade"]]
goat_score.drop(goat_score[goat_score.playerID != "jordami01"].index,inplace=True)
goat_score.reset_index()
goat_score = goat_score.groupby(["playerID"]).median().reset_index()
print(goat_score)




for i in range(0, len(goat_score.playerID)):
    if goat_score.playerID[i] == GOAT:
        categories = list(goat_score)[1:]
        N = len(categories)

            # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * math.pi for n in range(N)]
        angles += angles[:1]

            # Initialise the spider plot
        ax = plt.subplot(111, polar=True)

            # If you want the first axis to be on top:
        ax.set_theta_offset(math.pi / 2)
        ax.set_theta_direction(-1)

            # Draw one axe per variable + add labels labels yet
        plt.xticks(angles[:-1], categories)

            # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([250,500,750,1000,1250,1500,1750,2000,2250,2500], ["250","500","750","1000","1250","1500","1750","2000","2250","2500"], color="grey", size=7)
        plt.ylim(0, 2500)

            # ------- PART 2: Add plots

            # Plot each individual = each line of the data
            # I don't do a loop, because plotting more than 3 groups makes the chart unreadable

            # Ind1

        values = goat_score.loc[i].drop('playerID').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label="group A")
        ax.fill(angles, values, 'b', alpha=0.1)
            #plt.legend(df.playerID[i],loc='upper right', bbox_to_anchor=(0.1, 0.1))
        blue = mpatches.Patch(color='blue', label=goat_score.playerID[i])
        plt.legend(handles=[blue])
        plt.show()
        break

#================================================================4.2 and 4.3================================================================
nba_df = pd.merge(players,master,how="left",left_on="playerID",right_on="bioID")
print(nba_df.columns)


#nba_dfloc = nba_df[['playerID','birthState','year']].groupby(['birthState','playerID']).mean().reset_index()
#print(nba_dfloc)

asd= nba_df[["playerID","points","rebounds","assists","steals","blocks","fgMade","threeMade","birthState","birthCountry"]]
asd = asd[asd.birthCountry == "USA"]
print(asd)
#goat_df.columns = [["playerID","points/game","rebounds/game","assists/game","steals/game","blocks/game","fgMade/game","threeMade/game","GP"]]
asd = asd.groupby(['birthState','playerID']).sum().reset_index()
asd = asd.sort_values(['points'],ascending=False).reset_index()
asd = asd[0:10]
print(asd)

ax = sns.barplot(x="birthState",y = "points",hue = "playerID",data=asd)
plt.legend('')
plt.show()

#.sort_values(["score"],ascending = False).reset_index()
#pd.set_option('display.max_columns', None)
#asd = asd[asd.birthState == "NC"]
#print(asd)
"""
"""
nba_df = nba_df[nba_df.birthCountry == 'USA']
nba_df = nba_df[nba_df.birthDate != "0000-00-00"]
nba_df = nba_df[nba_df.height > 0]
print(nba_df)
nba_df['born_year'] = pd.DatetimeIndex(nba_df['birthDate']).year
nba_df['age'] = nba_df['year']-nba_df['born_year']
print(nba_df)
nba_ht = nba_df[['points','rebounds','assists','age','playerID','pos','birthState','year','height','threeMade','steals']]
print(nba_ht)
print(nba_ht.corr(method='pearson'))


#ax = sns.heatmap(heat_data,cmap="YlGnBu",linewidths=.5)

test = nba_df[['points','rebounds','assists','height']]
"""
corr = test.corr()
corr[np.abs(corr)<.2] = 0
plt.figure(figsize=(5,5))
sns.heatmap(corr,
            vmin=-1,
            vmax=1,
            cmap='coolwarm',
            annot=True)


plt.show()
"""
heat_data = pd.pivot_table(nba_ht,values = 'threeMade',index='height',columns='pos')
"""
ax = sns.heatmap(heat_data,cmap="YlGnBu",linewidths=.5)

plt.show()

heat_data = pd.pivot_table(nba_ht,values = 'assists',index='height',columns='pos')
ax = sns.heatmap(heat_data,cmap="YlGnBu",linewidths=.5)

plt.show()

heat_data = pd.pivot_table(nba_ht,values = 'steals',index='height',columns='pos')
ax = sns.heatmap(heat_data,cmap="YlGnBu",linewidths=.5)

plt.show()
"""
heat_data = pd.pivot_table(nba_ht,values = 'rebounds',index='height',columns='pos')
heat_data = pd.pivot_table(nba_ht,values = 'height',index='year',columns='pos')
ax = sns.heatmap(heat_data,cmap="YlGnBu",linewidths=.5)

plt.show()

