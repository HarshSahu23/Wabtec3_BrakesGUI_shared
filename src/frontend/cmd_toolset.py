# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# from collections import Counter

# def analyze_csv_files(folder_path):
#     if not os.path.exists(folder_path):
#         print(f"Folder '{folder_path}' does not exist.")
#         return

#     csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
#     if not csv_files:
#         print(f"No CSV files found in the folder '{folder_path}'.")
#         return

#     # If we want to plot a graph on the CSV file itself
#     # for file in csv_files:
#     #     file_path = os.path.join(folder_path, file)
#     #     print(f"\nProcessing file: {file}")

#     #     try:
#     #         # Load CSV
#     #         df = pd.read_csv(file_path)

#     #         # Check if 'description' column exists
#     #         if 'Description' not in df.columns:
#     #             print("Column 'Description' not found. Skipping this file.")
#     #             continue

#     #         # Count frequencies
#     #         frequencies = Counter(df['Description'].dropna())
#     #         table_data = frequencies.most_common()

#     #         # Display table
#     #         print("\nFrequency Table:")
#     #         print(f"{'Item':<30}{'Frequency':<10}")
#     #         print("-" * 40)
#     #         for item, count in table_data:
#     #             print(f"{item:<30}{count:<10}")

#     #         # Display ASCII graph
#     #         print("\nGraph Representation:")
#     #         max_label_width = 30
#     #         max_bar_width = 40  # Adjust for terminal width
#     #         max_count = max(frequencies.values())

#     #         for item, count in table_data:
#     #             label = item[:max_label_width] + ("..." if len(item) > max_label_width else "")
#     #             bar_length = int((count / max_count) * max_bar_width)
#     #             bar = "#" * bar_length
#     #             print(f"{label:<{max_label_width}} | {bar} ({count})")

#     #     except Exception as e:
#     #         print(f"Error processing file '{file}': {e}")


#     #If we want to display a graph using matplotlib and there is a save to local system

#     for file in csv_files:
#         file_path = os.path.join(folder_path, file)
#         print(f"\nProcessing file: {file}")

#         try:
#             df = pd.read_csv(file_path)

#             # Convert all column names to lowercase for case-insensitive comparison
#             if 'description'.lower() not in [col.lower() for col in df.columns]:
#                 print("Column 'description' not found. Skipping this file.")
#                 continue

#             # Count frequencies
#             frequencies = Counter(df['description'].dropna())
#             table_data = frequencies.most_common()

#             # Display table
#             print("\nFrequency Table:")
#             print(f"{'Item':<30}{'Frequency':<10}")
#             print("-" * 40)
#             for item, count in table_data:
#                 print(f"{item:<30}{count:<10}")

#             # Plot graph
#             items, counts = zip(*table_data)
#             plt.figure(figsize=(10, 6))
#             plt.bar(items, counts, color='skyblue')
#             plt.xlabel('Items', fontsize=12)
#             plt.ylabel('Frequency', fontsize=12)
#             plt.title(f'Frequency of Items in {file}', fontsize=14)
#             plt.xticks(rotation=45, ha='right')
#             plt.tight_layout()
#             plt.show()

#         except Exception as e:
#             print(f"Error processing file '{file}': {e}")

        
        

# if __name__ == "__main__":
#     print("Welcome to CMD Toolset")
#     folder_path = input("Enter the folder path containing CSV files: ").strip()
#     analyze_csv_files(folder_path)

import os
import sys
sys.path.append('../')
import pandas as pd
from tabulate import tabulate
from backend.data_handler import DataHandler
from backend.plotter import Plotter
# import src.backend.data_handler as bbm

def main():
    print("Welcome to CMD Toolset")
    folder_path = input("Enter the folder path containing CSV files: ").strip()
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    # Initialize DataHandler
    DH = DataHandler(folder_path)
    summary_df = DH.ecl_freq_summary  # DataHandler returns a DataFrame with 'Description' and 'Frequency'

    if summary_df.empty:
        print("No data to process.")
        return

    # Display the initial summary table
    print("\nSummary Table:")
    print(tabulate(summary_df, headers='keys', tablefmt='grid'))

    while True:
        command = input("\nEnter a command (show summary, bar_chart <tags>, pie_chart <tags>, exit): ").strip()
        if command.lower() == "exit":
            print("Exiting CMD Toolset.")
            break

        elif command.lower() == "show summary":
            print("\nSummary Table:")
            print(tabulate(summary_df, headers='keys', tablefmt='grid'))

        elif command.startswith("bar_chart"):
            try:
                tags = command.split(" ", 1)[1].split()
                filtered_df = summary_df[summary_df['Description'].isin(tags)]
                if filtered_df.empty:
                    print(f"No matching tags found for: {tags}")
                else:
                    Plotter.plot_bar_chart(
                        x=filtered_df['Description'].tolist(),
                        y=filtered_df['Frequency'].tolist(),
                        xlabel="Description",
                        ylabel="Frequency"
                    )
            except IndexError:
                print("Please specify tags for the bar chart (e.g., bar_chart tag1 tag2).")

        elif command.startswith("pie_chart"):
            try:
                tags = command.split(" ", 1)[1].split()
                filtered_df = summary_df[summary_df['Description'].isin(tags)]
                if filtered_df.empty:
                    print(f"No matching tags found for: {tags}")
                else:
                    Plotter.plot_pie_chart(
                        labels=filtered_df['Description'].tolist(),
                        data=filtered_df['Frequency'].tolist()
                    )
            except IndexError:
                print("Please specify tags for the pie chart (e.g., pie_chart tag1 tag2).")

        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()



