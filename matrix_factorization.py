'''
***NOTE***
We chose not to use this matrix factorization as another metric in our submission because we did not have time to fully
finish the method. Nevertheless, we include the code in our submission as a demonstration of our
thought process as well as an example of another thing we worked on during the hackathon.


Offensive / Defensive Traits Extraction by
Matrix Factorization


Joint estimation of the Offensive and Defensive latent vectors (U and V) at the same time with only data of the final scores. 

Team M’s score when playing against Team N, denoted by S_mn, can be factorized into the sum of scores gained from a few tactics (latent dimension l). 
Note, If Offensive (of Team M in tactic l) is strong then U_ml is big, while the opposite is true for Defensive,  Defensive (of Team N in tactic l) is weak then V_ln is big.

** Adams, Ryan Prescott, George E. Dahl, and Iain Murray. "Incorporating side information in probabilistic matrix factorization with gaussian processes."arXiv preprint arXiv:1003.4944 (2010).


We can do more... (with more time and data)

1. Improve the resolution to all players’ offensive and defensive latent embedding. (with a full Bayesian data augmentation techniques if we have the data available, methodology see ref. 1)
2. Incorporate the side information by imposing related prior on Factored Matrices (methodology see ref. 2)

Ref1. 
Malecki, Michael. "An Ecological Item-Response Model for Multiple Subsets of Respondents with Application to the European Court of Justice." Available at SSRN 1441414 (2009).

Ref2.
Adams, Ryan Prescott, George E. Dahl, and Iain Murray. "Incorporating side information in probabilistic matrix factorization with gaussian processes."arXiv preprint arXiv:1003.4944 (2010).



'''


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.mplot3d import Axes3D

# get data
df_pbp = pd.read_table("data/Hackathon_play_by_play.txt", delim_whitespace=True)
df_team_ids = pd.read_table("data/Hackathon_teamid_link.txt", delim_whitespace=True)

# get rows with final scores
indices = df_pbp.loc[df_pbp['Event_Num'] == 1].index.tolist()
indices_true = [x - 1 for x in indices]

# we don't want the 0th row
indices_true.pop(0)

# the last row is also a final score
indices_true.append(df_pbp.shape[0])

# get new dataframe with only the rows/cols we want
df_scores = df_pbp.ix[indices_true][['Home_PTS','Visitor_PTS', 'Home_Team_id', 'Away_Team_id']]

# create an empty matrix, each row and col represent an NBA team
scores = np.zeros((30,30))
team_list = [x for x in range(0,30)]
df_scores_mat = pd.DataFrame(data=scores, columns=team_list)

# Populate our empty matrix with the cumulative scores between teams
for index, row in df_scores.iterrows():
    
    # get id
    home_id = row['Home_Team_id']
    away_id = row['Away_Team_id']
    
    # convert id to a number in range 0-29
    home_num = df_team_ids.loc[df_team_ids['TEAM_ID'] == home_id]['SV_TEAM_ID']
    away_num = df_team_ids.loc[df_team_ids['TEAM_ID'] == away_id]['SV_TEAM_ID']
    home_num = home_num.iloc[0]
    away_num = away_num.iloc[0]
    
    # add scores to matrix
    df_scores_mat[home_num][away_num] += row['Home_PTS']
    df_scores_mat[away_num][home_num] += row['Visitor_PTS']

scores_mat = df_scores_mat.as_matrix()

# apply SVD
from scipy.sparse.linalg import svds
U, s, V = svds(scores_mat,k=2)

# plot latent vectors
plt.scatter(U[:,0], U[:,1], c=np.arange(0,30))
plt.show()

# scale by eigenvalues and plot again
U2 = np.dot(U,np.sqrt(np.diag(s)))
plt.scatter(U2[:,0], U2[:,1], c=np.arange(0,30))
plt.show()