import os
import sys
sys.path.append('../')
# import pandas as pd
from tabulate import tabulate
from backend.data_handler import DataHandler
from backend.plotter import Plotter

def show_help():
    help_text = """
    Available commands:
    
    1. show summary
        - Displays the summary table of descriptions and their frequencies.

    2. bar_chart <tags>
        - Displays a bar chart for specified tags.
        - Example: bar_chart tag1 tag2

    3. pie_chart <tags>
        - Displays a pie chart for specified tags.
        - Example: pie_chart tag1 tag2

    4. barchart
        - Displays a bar chart for all descriptions and their frequencies.

    5. piechart
        - Displays a pie chart for all descriptions and their frequencies.

    6. help
        - Shows this help message with available commands.

    7. exit
        - Exits the CMD Toolset.
    """
    print(help_text)

def main():
    print("Welcome to CMD Toolset")

    # Take the folder path input first, no commands shown yet
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

    # Now, the user can type commands

    while True:
        command = input("\nEnter a command (type 'help' for a list of available commands): ").strip()

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

        elif command.lower() == "barchart":
            Plotter.plot_bar_chart(
                x=summary_df['Description'].tolist(),
                y=summary_df['Frequency'].tolist(),
                xlabel="Description",
                ylabel="Frequency"
            )
            print("Whole frequency bar chart created.")

        elif command.lower() == "piechart":
            Plotter.plot_pie_chart(
                labels=summary_df['Description'].tolist(),
                data=summary_df['Frequency'].tolist()
            )
            print("Whole frequency pie chart created.")

        elif command.lower() == "help":
            show_help()

        else:
            print("Invalid command. Type 'help' to see the available options.")

if __name__ == "__main__":
    main()
