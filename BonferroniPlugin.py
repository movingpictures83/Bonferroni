from scipy.stats import spearmanr
import pandas as pd
from statsmodels.stats.multitest import multipletests
import numpy as np


def calc_spearman(dataPath):
    df = pd.read_csv(dataPath, index_col=0)
    df = df.astype(float)
    cols = list(df.columns)
    sp, p = spearmanr(df)
    sp_df, p_df = pd.DataFrame(sp, columns=cols, index=cols), pd.DataFrame(p, columns=cols, index=cols)
    sp_df, p_df = sp_df.fillna(0), p_df.fillna(1) # If abundance was constant - correlation will be NaN
    return sp_df, p_df


def correct_p_val(sp_df, p_df, to_file="False", method="bonferroni"):
    # Returns Spearman correlation filtered by Bonferroni correction
    p_corrected_df = p_df.apply(lambda x: multipletests(x, method=method, alpha=0.05)[0])
    #p_corrected_df = p_df
    cols = sp_df.columns
    sp_corrected = sp_df.where(p_corrected_df, other=0)
    print("We selected {} p_values".format(p_corrected_df.values.sum() - len(p_corrected_df)))

    if to_file!="False":
        sp_corrected.to_csv(to_file, index=True)
    return sp_corrected


def add_quote(in_file, out_file):
    i=0
    with open(in_file, "r") as in_f:
        with open(out_file, "w") as out_f:
            for line in in_f.readlines():
                if i==0:
                    line=line.strip("\n")
                    columns = line.split(",")
                    out_line = ""
                    for col in columns:
                        if '"' not in col:
                            out_line += '"' + col + '",'
                        else:
                            out_line += col + ","
                    out_line = out_line.strip(',')
                    out_line+="\n"
                else:
                    line = line.strip("\n")
                    columns = line.split(",")
                    out_line = ""
                    for j, col in enumerate(columns):
                        if j==0:
                            out_line += '"' + col + '",'
                        else:
                            out_line += col + ','
                    out_line = out_line.strip(',')
                    out_line += "\n"
                out_f.write(out_line)
                i+=1

#if __name__=="__main__":

    # nonUsersPath = "/Users/stebliankin/Desktop/MASH-CohortProject/Co-Occurrence/MultiOmics_nonUsers.csv"
    # usersPath = "/Users/stebliankin/Desktop/MASH-CohortProject/Co-Occurrence/MultiOmics_users.csv"
    #
    # out_spearmanUsers = "/Users/stebliankin/Desktop/MASH-CohortProject/Co-Occurrence/PLUMA-corrected/spearmanCorrectedUsers.csv"
    # out_spearmanNonUsers = "/Users/stebliankin/Desktop/MASH-CohortProject/Co-Occurrence/PLUMA-corrected/spearmanCorrectedNonUsers.csv"
    #
    # # Users
    # sp_df, p_df = calc_spearman(usersPath)
    # sp_df = correct_p_val(sp_df, p_df, to_file=out_spearmanUsers)
    #
    # # Non users:
    # sp_df, p_df = calc_spearman(nonUsersPath)
    # sp_df = correct_p_val(sp_df, p_df, to_file=out_spearmanNonUsers)
    #
    # # Step 2 - add quotes to the first line to be able to run PLUMA
    #
    # import os
    # in_folder = "/Users/stebliankin/Desktop/MASH-CohortProject/Co-Occurrence/PLUMA-corrected"
    # out_folder = "/Users/stebliankin/Desktop/MASH-CohortProject/Co-Occurrence/PLUMA-corrected/results"
    #
    # if not os.path.exists(out_folder):
    #     os.mkdir(out_folder)
    #
    # files = os.listdir(in_folder)
    #
    # for f in files:
    #     if f!= ".DS_Store" and f!="results":
    #         try:
    #             in_file = os.path.join(in_folder, f)
    #             out_file = os.path.join(out_folder, f)
    #             add_quote(in_file, out_file)
    #         except IsADirectoryError:
    #             pass
class BonferroniPlugin:
  def input(self, inputfile):
    #nonUsersPath = "MultiOmics_nonUsers.csv"
    self.usersPath = inputfile

  def run(self):
    pass

  def output(self, outputfile):
    out_spearmanUsers = outputfile#"spearmanCorrectedUsers.csv"
    #out_spearmanNonUsers = "spearmanCorrectedNonUsers.csv"

    # Users
    sp_df, p_df = calc_spearman(self.usersPath)
    sp_df = correct_p_val(sp_df, p_df, to_file=out_spearmanUsers, method="fdr_bh")

    # Non users:
    #sp_df, p_df = calc_spearman(nonUsersPath)
    #sp_df = correct_p_val(sp_df, p_df, to_file=out_spearmanNonUsers, method="fdr_bh")
3
    # Step 2 - add quotes to the first line to be able to run PLUMA

    #import os
    #in_folder = "/Users/stebliankin/Desktop/MASH-CohortProject/Co-Occurrence/PLUMA-corrected/BenjaminHochberg"
    #out_folder = "/Users/stebliankin/Desktop/MASH-CohortProject/Co-Occurrence/PLUMA-corrected/BenjaminHochberg/results/"

    #if not os.path.exists(out_folder):
    #    os.mkdir(out_folder)

    #files = os.listdir(in_folder)

    #for f in files:
    #    if f!= ".DS_Store" and f!="results":
    #        try:
    #            in_file = os.path.join(in_folder, f)
    #            out_file = os.path.join(out_folder, f)
    #            add_quote(in_file, out_file)
    #        except IsADirectoryError:
    #            pass
