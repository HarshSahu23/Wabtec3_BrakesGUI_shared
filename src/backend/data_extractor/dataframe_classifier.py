import logging
import pandas as pd
from enum import Enum

class DataFrameClasses(Enum):
    ECL = 1
    DMP = 2
    UNKNOWN = 3

 
class DataFrameClassifier:
    @staticmethod
    def get_dataframe_class(df: pd.DataFrame = None):
        """
        Determine file class with more robust type detection.
        
        Args:
            file_path (str): Path to the CSV file
        
        Returns:
            FileClasses: Detected file class
        """
        try:
            # Validate readability
            if df.empty:
                logging.warning(f"Empty dataframe passed. Unable to classify.")
                return DataFrameClasses.UNKNOWN

            first_row = df.iloc[0]  # Get the first row
            all_numeric = first_row.apply(lambda x: x.isnumeric() if isinstance(x, str) else isinstance(x, (int, float))).all()
            if all_numeric:
                return DataFrameClasses.DMP
            else:
                return DataFrameClasses.ECL
            # Implement UNKNOWN condition
            # return DataFrameClasses.UNKNOWN

        except Exception as e:
            logging.error(f"Unexpected error in file classification: {e}")
            return DataFrameClasses.UNKNOWN

