import pandas as pd
import glob
import os
import logging
from tqdm import tqdm
from enum import Enum
import tabulate

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('data_handler.log'),
        logging.StreamHandler()
    ]
)

class FileProcessingError(Exception):
    """Custom exception for file processing errors."""
    pass

class FileClasses(Enum):
    ECL_ECF = 1
    DMP_LOG = 2
    UNKNOWN = 3

class DataHandler:
    def __init__(self, folder_path):
        """
        Initialize DataHandler with robust folder path validation.
        
        Args:
            folder_path (str): Path to the folder containing CSV files
        
        Raises:
            FileNotFoundError: If the folder does not exist
            PermissionError: If there are permission issues accessing the folder
        """
        try:
            # Validate folder path
            if not os.path.exists(folder_path):
                raise FileNotFoundError(f"Folder path does not exist: {folder_path}")
            
            if not os.path.isdir(folder_path):
                raise NotADirectoryError(f"Provided path is not a directory: {folder_path}")
            
            # Validate read permissions
            if not os.access(folder_path, os.R_OK):
                raise PermissionError(f"No read permissions for folder: {folder_path}")
            
            self.__folder_path = folder_path
            self.ecl = pd.DataFrame()
            self.ecf = pd.DataFrame()
            self.dmp = pd.DataFrame()
            self.ecl_freq_summary = pd.DataFrame()
            self.filtered_dmp = pd.DataFrame()
            self.dmp_freq_summary = pd.DataFrame()
            
            # Process files with error handling
            self.set_folder(folder_path)
            
        except (FileNotFoundError, PermissionError, NotADirectoryError) as e:
            logging.error(f"Initialization error: {e}")
            raise

    def __format_ecl(self, df_ecl):
        """
        Format ECL dataframe with robust error handling.
        
        Args:
            df_ecl (pd.DataFrame): Input dataframe
        
        Returns:
            pd.DataFrame: Formatted dataframe
        
        Raises:
            FileProcessingError: If formatting fails
        """
        try:
            if df_ecl is None or df_ecl.empty:
                raise ValueError("Input dataframe is empty or None")
            
            # Skip some rows that are not required
            df_ecl_fmtd = df_ecl.iloc[8:].reset_index(drop=True)

            # Validate split operation
            try:
                df_ecl_fmtd = df_ecl_fmtd.iloc[:, 0].str.split(';', expand=True)
            except Exception as e:
                raise FileProcessingError(f"Failed to split ECL dataframe: {e}")

            # Ensure columns exist
            if df_ecl_fmtd.empty or len(df_ecl_fmtd.columns) < 2:
                raise FileProcessingError("Insufficient columns after splitting")

            # Reassign columns
            df_ecl_fmtd.columns = df_ecl_fmtd.iloc[0]

            # Drop unrequired columns
            df_ecl_fmtd = df_ecl_fmtd.drop(df_ecl_fmtd.columns[[0, -1]], axis=1)

            # Reset the index
            df_ecl_fmtd = df_ecl_fmtd.iloc[1:].reset_index(drop=True)

            return df_ecl_fmtd
        
        except (ValueError, FileProcessingError) as e:
            logging.error(f"ECL formatting error: {e}")
            return pd.DataFrame()

    def __format_ecf(self, df_ecf):
        """
        Format ECF dataframe with robust error handling.
        
        Args:
            df_ecf (pd.DataFrame): Input dataframe
        
        Returns:
            pd.DataFrame: Formatted dataframe
        
        Raises:
            FileProcessingError: If formatting fails
        """
        try:
            if df_ecf is None or df_ecf.empty:
                raise ValueError("Input dataframe is empty or None")
            
            # Skip some rows that are not required
            df_ecf_fmtd = df_ecf.iloc[1:].reset_index(drop=True)

            # Validate split operation
            try:
                df_ecf_fmtd = df_ecf_fmtd.iloc[:, 0].str.split(';', expand=True)
            except Exception as e:
                raise FileProcessingError(f"Failed to split ECF dataframe: {e}")

            # Ensure columns exist
            if df_ecf_fmtd.empty or len(df_ecf_fmtd.columns) < 2:
                raise FileProcessingError("Insufficient columns after splitting")

            # Reassign columns
            df_ecf_fmtd.columns = df_ecf_fmtd.iloc[0]

            # Drop unrequired columns
            df_ecf_fmtd = df_ecf_fmtd.drop(df_ecf_fmtd.columns[-1], axis=1)

            # Reset the index
            df_ecf_fmtd = df_ecf_fmtd.iloc[1:].reset_index(drop=True)

            return df_ecf_fmtd
        
        except (ValueError, FileProcessingError) as e:
            logging.error(f"ECF formatting error: {e}")
            return pd.DataFrame()

    def get_file_class(self, file_path):
        """
        Determine file class with more robust type detection.
        
        Args:
            file_path (str): Path to the CSV file
        
        Returns:
            FileClasses: Detected file class
        """
        try:
            # Validate file existence and readability
            if not os.path.exists(file_path):
                logging.warning(f"File does not exist: {file_path}")
                return FileClasses.UNKNOWN
            
            if not os.access(file_path, os.R_OK):
                logging.warning(f"Cannot read file: {file_path}")
                return FileClasses.UNKNOWN

            # Read with error handling
            try:
                df = pd.read_csv(file_path, nrows=50, low_memory=False)
            except Exception as e:
                logging.error(f"Error reading file {file_path}: {e}")
                return FileClasses.UNKNOWN

            file_type_and_col_names = {
                FileClasses.ECL_ECF: ["ERROR CODE LISTING", "Code(hex)", "Ticks(hex)"],
                FileClasses.DMP_LOG: ["MOD_TICK", "MONTIME"]
            }

            # Strict and sensitive column matching
            for column_name in df.columns:
                for file_class, column_list in file_type_and_col_names.items():
                    if any(col in column_name for col in column_list):
                        return file_class
            
            return FileClasses.UNKNOWN

        except Exception as e:
            logging.error(f"Unexpected error in file classification: {e}")
            return FileClasses.UNKNOWN

    def read_dmp_from_csv_file(self, file_path):
        """
        Read DMP file with comprehensive error handling.
        
        Args:
            file_path (str): Path to the CSV file
        
        Returns:
            pd.DataFrame: Loaded dataframe or empty dataframe
        """
        try:
            data = pd.read_csv(file_path, low_memory=False)
            
            # Additional validation
            if data.empty:
                logging.warning(f"Empty dataframe from file: {file_path}")
            
            return data
        
        except pd.errors.EmptyDataError:
            logging.error(f"No columns to parse from file: {file_path}")
            return pd.DataFrame()
        except pd.errors.ParserError as e:
            logging.error(f"Parsing error in file {file_path}: {e}")
            return pd.DataFrame()
        except Exception as e:
            logging.error(f"Unexpected error reading DMP file {file_path}: {e}")
            return pd.DataFrame()

    def read_ecl_ecf_from_csv_file(self, file_path):
        """
        Read and format ECL and ECF from CSV with robust error handling.
        
        Args:
            file_path (str): Path to the CSV file
        
        Returns:
            tuple: Formatted ECL and ECF dataframes
        """
        try:
            data = pd.read_csv(file_path, low_memory=False)

            if data.empty:
                logging.warning(f"Empty dataframe from file: {file_path}")
                return pd.DataFrame(), pd.DataFrame()

            # More robust index finding
            ecf_indices = data[data.iloc[:, 0].str.contains("ERROR CODE FREQUENCY", na=False)].index
            if len(ecf_indices) == 0:
                logging.warning(f"No ECF section found in file: {file_path}")
                return pd.DataFrame(), pd.DataFrame()

            ecf_index = ecf_indices[0]

            df_ecl = data.iloc[0:ecf_index, ]
            df_ecf = data.iloc[ecf_index:, ]

            df_ecl = self.__format_ecl(df_ecl)
            df_ecf = self.__format_ecf(df_ecf)

            return df_ecl, df_ecf

        except Exception as e:
            logging.error(f"Error processing ECL/ECF file {file_path}: {e}")
            return pd.DataFrame(), pd.DataFrame()

    def read_csv_from_folder(self, folder_path):
        """
        Read and merge CSV files from folder with comprehensive error handling.
        
        Args:
            folder_path (str): Path to the folder containing CSV files
        
        Returns:
            tuple: Merged ECL, ECF, and DMP dataframes
        """
        merged_df_ecl = pd.DataFrame()
        merged_df_ecf = pd.DataFrame()
        merged_dmp = pd.DataFrame()

        try:
            csv_files = glob.glob(f"{folder_path}/*.csv")
            
            if not csv_files:
                logging.warning(f"No CSV files found in folder: {folder_path}")
                return merged_df_ecl, merged_df_ecf, merged_dmp

            for csv_file_path in tqdm(csv_files, desc="Reading Files"):
                try:
                    file_type = self.get_file_class(csv_file_path)
                    
                    if file_type == FileClasses.ECL_ECF:
                        df_ecl, df_ecf = self.read_ecl_ecf_from_csv_file(csv_file_path)
                        
                        if not df_ecl.empty:
                            merged_df_ecl = pd.concat([merged_df_ecl, df_ecl])
                        if not df_ecf.empty:
                            merged_df_ecf = pd.concat([merged_df_ecf, df_ecf])
                    
                    elif file_type == FileClasses.DMP_LOG:
                        df_dmp = self.read_dmp_from_csv_file(csv_file_path)
                        
                        if not df_dmp.empty:
                            merged_dmp = pd.concat([merged_dmp, df_dmp])
                    
                    else:
                        logging.warning(f"Skipping unrecognized file: {csv_file_path}")

                except Exception as file_error:
                    logging.error(f"Error processing file {csv_file_path}: {file_error}")
                    continue

            # Reset indices safely
            merged_df_ecf.reset_index(drop=True, inplace=True)
            merged_df_ecl.reset_index(drop=True, inplace=True)
            merged_dmp.reset_index(drop=True, inplace=True)

            return merged_df_ecl, merged_df_ecf, merged_dmp

        except Exception as e:
            logging.error(f"Unexpected error reading CSV files: {e}")
            return merged_df_ecl, merged_df_ecf, merged_dmp

    def get_ecl_freq_summary(self, df_ecl_fmtd):
        """
        Get ECL frequency summary with error handling.
        
        Args:
            df_ecl_fmtd (pd.DataFrame): Formatted ECL dataframe
        
        Returns:
            pd.DataFrame: Summary dataframe
        """
        try:
            if df_ecl_fmtd is None or df_ecl_fmtd.empty:
                logging.warning("Empty or None dataframe passed to get_ecl_freq_summary")
                return pd.DataFrame()

            summary = df_ecl_fmtd.groupby(by=["Description"])
            summary = summary.size().reset_index(name='Frequency')
            summary['SortKey'] = summary['Description'].apply(lambda x: (-len(str(x)), str(x).lower()))
            summary = summary.sort_values(by="SortKey", ignore_index=True)
            summary = summary.drop(columns='SortKey')
            
            return summary
        
        except Exception as e:
            logging.error(f"Error generating ECL frequency summary: {e}")
            return pd.DataFrame()

    def get_dmp_freq_summary(self, df_dmp):
        """
        Get DMP frequency summary with error handling.
        
        Args:
            df_dmp (pd.DataFrame): Filtered DMP dataframe
        
        Returns:
            pd.Series: Frequency summary
        """
        try:
            if df_dmp is None or df_dmp.empty:
                logging.warning("Empty or None dataframe passed to get_dmp_freq_summary")
                return pd.Series()

            summary = df_dmp.sum(axis=0)
            return summary
        
        except Exception as e:
            logging.error(f"Error generating DMP frequency summary: {e}")
            return pd.Series()

    def set_folder(self, folder_path):
        """
        Set folder and process files with comprehensive error handling.
        
        Args:
            folder_path (str): Path to the folder containing CSV files
        """
        try:
            self.__folder_path = folder_path
            self.ecl, self.ecf, self.dmp = self.read_csv_from_folder(self.__folder_path)
            
            # Validate processing results
            if self.ecl.empty:
                logging.warning("No ECL data processed")
            if self.ecf.empty:
                logging.warning("No ECF data processed")
            if self.dmp.empty:
                logging.warning("No DMP data processed")

            self.ecl_freq_summary = self.get_ecl_freq_summary(self.ecl)
            
            self.filtered_dmp = self.filter_dmp(self.dmp)
            self.dmp_freq_summary = self.get_dmp_freq_summary(self.filtered_dmp)
            
        except Exception as e:
            logging.error(f"Error setting folder: {e}")
            # Reset to empty state if processing fails
            self.ecl = pd.DataFrame()
            self.ecf = pd.DataFrame()
            self.dmp = pd.DataFrame()
            self.filtered_dmp = pd.DataFrame()
            self.dmp_freq_summary = pd.Series()

    def get_folder(self):
        return self.__folder_path

    def filter_dmp(self, df_dmp):
        """
        Filter DMP dataframe with robust error handling.
        
        Args:
            df_dmp (pd.DataFrame): Input DMP dataframe
        
        Returns:
            pd.DataFrame: Filtered dataframe
        """
        try:
            if df_dmp is None or df_dmp.empty:
                logging.warning("Empty or None dataframe passed to filter_dmp")
                return pd.DataFrame()

            required_columns = ["FILL_1","VENT_1","FILL_2","VENT_2","FILL_3","VENT_3","FILL_4","VENT_4"]
            
            # Check if all required columns exist
            missing_columns = [col for col in required_columns if col not in df_dmp.columns]
            if missing_columns:
                logging.warning(f"Missing columns in DMP: {missing_columns}")
                return pd.DataFrame()

            f_df_dmp = df_dmp[required_columns]
            f_df_dmp = f_df_dmp.loc[:, (f_df_dmp[required_columns] != 0).any(axis=0)]
            
            return f_df_dmp
        
        except Exception as e:
            logging.error(f"Error filtering DMP dataframe: {e}")
            return pd.DataFrame()

if __name__ == "__main__":
    try:
        folder_path = "csv"
        
        # Validate folder path before processing
        if not os.path.exists(folder_path):
            print(f"Error: Folder {folder_path} does not exist.")
            sys.exit(1)
        
        dh = DataHandler(folder_path)
        
        # Optional: Additional logging or validation of processed data
        print("Data processed successfully.")
        print(f"ECL Rows: {len(dh.ecl)}")
        print(f"ECF Rows: {len(dh.ecf)}")
        print(f"DMP Rows: {len(dh.dmp)}")
        
    except Exception as e:
        logging.error(f"Critical error in main execution: {e}")
        print("Data processing failed. Check logs for details.")