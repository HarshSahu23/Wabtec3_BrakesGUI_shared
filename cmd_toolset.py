import os
import sys
import pandas as pd
from tabulate import tabulate
from src.backend.data_handler import DataHandler
from src.backend.plotter import Plotter

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



