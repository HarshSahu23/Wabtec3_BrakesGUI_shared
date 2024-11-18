import pandas as pd
import glob
from tqdm import tqdm
from enum import Enum
import tabulate

class FileClasses(Enum):
    ECL_ECF = 1
    DMP_LOG = 2

class DataHandler:
    # __folder_path = ""
    # ecl = pd.DataFrame()
    # ecf = pd.DataFrame()
    # ecl_freq_summary = pd.DataFrame()
    __file_classes = []
    def __format_ecl(self, df_ecl):
        # Skip some rows that are not required
        df_ecl_fmtd = df_ecl.iloc[8:].reset_index(drop=True)

        # Split the text into separate with ';' as delimiter
        df_ecl_fmtd = df_ecl_fmtd.iloc[:, 0].str.split(';', expand=True)

        # Reassign columns
        df_ecl_fmtd.columns = df_ecl_fmtd.iloc[0]

        # Drop unrequired columns
        df_ecl_fmtd = df_ecl_fmtd.drop(df_ecl_fmtd.columns[[0, -1]], axis=1)

        # Reset the index
        df_ecl_fmtd = df_ecl_fmtd.iloc[1:].reset_index(drop=True)

        return df_ecl_fmtd

    def __format_ecf(self, df_ecf):
        # Skip some rows that are not required
        df_ecf_fmtd = df_ecf.iloc[1:].reset_index(drop=True)

        # Split the text into separate with ';' as delimiter
        df_ecf_fmtd = df_ecf_fmtd.iloc[:, 0].str.split(';', expand=True)

        # Reassign columns
        df_ecf_fmtd.columns = df_ecf_fmtd.iloc[0]

        # Drop unrequired columns
        df_ecf_fmtd = df_ecf_fmtd.drop(df_ecf_fmtd.columns[-1], axis=1)

        # Reset the index
        df_ecf_fmtd = df_ecf_fmtd.iloc[1:].reset_index(drop=True)

        return df_ecf_fmtd


    def get_file_class(self, file_path):
        df = pd.read_csv(file_path, nrows=50)

        file_type_and_col_names = {
            FileClasses.ECL_ECF : ["ERROR CODE LISTING", "Code(hex)", "Ticks(hex)"],
            FileClasses.DMP_LOG : ["MOD_TICK", "MONTIME"]
        }

        for column_name in df.columns:
            for file_class, column_list in file_type_and_col_names.items():
                for column in column_list:
                    if(column_name.find(column) != -1):
                        return file_class
    
    
    # Error_log_dump_reader CSV reader
    def read_dmp_from_csv_file(self, file_path):
        data = pd.read_csv(file_path)
        return data

    # Read and format dataframe from file_path provided
    def read_ecl_ecf_from_csv_file(self, file_path):
        data = pd.read_csv(file_path)

        ecf_index = data[data.iloc[:, 0].str.contains(
            "ERROR CODE FREQUENCY")].index[0]

        df_ecl = data.iloc[0:ecf_index, ]
        df_ecf = data.iloc[ecf_index:, ]

        df_ecl = self.__format_ecl(df_ecl)
        df_ecf = self.__format_ecf(df_ecf)

        return df_ecl, df_ecf
    

    # Read, format and merge dataframe from files under folder_path provided
    def read_csv_from_folder(self, folder_path):
        csv_files = glob.glob(f"{folder_path}/*.csv")
        merged_df_ecl = pd.DataFrame()
        merged_df_ecf = pd.DataFrame()
        merged_dmp = pd.DataFrame()

        for csv_file_path in tqdm(csv_files, desc="Reading Files"):
            file_type = self.get_file_class(csv_file_path)
            if(file_type == FileClasses.ECL_ECF):
                df_ecl, df_ecf = self.read_ecl_ecf_from_csv_file(csv_file_path)
                merged_df_ecl = pd.concat([merged_df_ecl, df_ecl])  # Default axis = 0
                merged_df_ecf = pd.concat([merged_df_ecf, df_ecf])  # Default axis = 0
            else:
                df_dmp = self.read_dmp_from_csv_file(csv_file_path)
                merged_dmp = pd.concat([merged_dmp, df_dmp])

        merged_df_ecf.reset_index(drop=True, inplace=True)
        merged_df_ecl.reset_index(drop=True, inplace=True)
        merged_dmp.reset_index(drop=True, inplace=True)

        return merged_df_ecl, merged_df_ecf, merged_dmp

    def get_ecl_freq_summary(self, df_ecl_fmtd):
        summary = df_ecl_fmtd.groupby(by=["Description"])
        summary = summary.size().reset_index(name='Frequency')
        summary['SortKey'] = summary['Description'].apply(lambda x: (-len(x), x.lower()))
        summary = summary.sort_values(by="SortKey", ignore_index=True)
        summary = summary.drop(columns='SortKey')
        return summary

    def get_dmp_freq_summary(self, df_dmp):
        summary = df_dmp.sum(axis=0)
        return summary

    def get_folder(self):
        return self.__folder_path

    def filter_dmp(self, df_dmp):
        required_columns = ["FILL_1","VENT_1","FILL_2","VENT_2","FILL_3","VENT_3","FILL_4","VENT_4"]
        f_df_dmp = df_dmp[required_columns]
        f_df_dmp = f_df_dmp.loc[:, (f_df_dmp[required_columns] != 0).any(axis=0)]
        return f_df_dmp


    def set_folder(self, folder_path):
        self.__folder_path = folder_path
        self.ecl = pd.DataFrame()
        self.ecf = pd.DataFrame()
        self.dmp = pd.DataFrame()
        self.ecl, self.ecf, self.dmp = self.read_csv_from_folder(self.__folder_path)
        self.ecl_freq_summary = self.get_ecl_freq_summary(self.ecl)
        self.filtered_dmp = self.filter_dmp(self.dmp)
        self.dmp_freq_summary = self.get_dmp_freq_summary(self.filtered_dmp)

    def __init__(self, folder_path):
        self.set_folder(folder_path)

if __name__ == "__main__":
    folder_path = "csv"
    dh = DataHandler(folder_path)
