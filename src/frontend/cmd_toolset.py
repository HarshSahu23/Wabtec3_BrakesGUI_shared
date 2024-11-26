import argparse
import shlex
import os
import sys

from tabulate import tabulate
from backend.data_handler import DataHandler
from backend.plotter import Plotter


def import_folder(folder_path=None):
    if not (os.path.exists(folder_path) and
            os.path.isdir(folder_path) and
            os.access(folder_path, os.R_OK)):
        raise ValueError(
            f"Invalid folder path: '{folder_path}'. Ensure it exists, is a directory, and is accessible.")
    print(f"Importing new folder...")
    print(f"Folder path: {folder_path}")
    dh = DataHandler(folder_path)
    return dh


def exit_cli():
    sys.exit(0)


def plot_bar(tags=None, dh: DataHandler = None):
    try:
        filtered_df = dh.ecl_freq_summary[dh.ecl_freq_summary['Description'].isin(
            tags)]
        if filtered_df.empty:
            print(f"No matching tags found for: {tags}")
        else:
            print("Drawing bar chart with given error names...")
            Plotter.plot_bar_chart(
                x=filtered_df['Description'],
                y=filtered_df['Frequency'],
                xlabel="Description",
                ylabel="Frequency"
            )
    except IndexError:
        print("Please specify tags for the bar chart (e.g., bar_chart tag1 tag2).")


def plot_pie(tags=None, dh: DataHandler = None):
    try:
        filtered_df = dh.ecl_freq_summary[dh.ecl_freq_summary['Description'].isin(
            tags)]
        if filtered_df.empty:
            print(f"No matching tags found for: {tags}")
        else:
            print("Drawing pie chart with given error names...")
            Plotter.plot_pie_chart(
                labels=filtered_df['Description'],
                data=filtered_df['Frequency']
            )
    except IndexError:
        print("Please specify tags for the pie chart (e.g., pie_chart tag1 tag2).")


def plot_complete_bar(dh: DataHandler):
    print("Drawing complete bar chart...")
    Plotter.plot_bar_chart(
        x=dh.ecl_freq_summary['Description'],
        y=dh.ecl_freq_summary['Frequency'],
        xlabel="Description",
        ylabel="Frequency"
    )


def plot_complete_pie(dh: DataHandler):
    print("Drawing complete pie chart...")
    Plotter.plot_pie_chart(
        labels=dh.ecl_freq_summary['Description'],
        data=dh.ecl_freq_summary['Frequency']
    )


def validate_data_handler(dh: DataHandler = None):
    if dh == None:
        raise ValueError(
            "The provided data handler object is None. Try importing first.")


def show_summary(dh: DataHandler):
    print("="*20 + "Summary Table" + "="*20)
    print(tabulate(dh.ecl_freq_summary, headers='keys', tablefmt='grid'))


def create_parser():
    """Create the argparse parser with subcommands."""
    parser = argparse.ArgumentParser(
        description="CLI tool for performing actions with options and parameters"
    )

    # Create subparsers for actions
    subparsers = parser.add_subparsers(
        dest="action", required=True, help="Available actions")

    # Subparser for action 'import'
    parser_one = subparsers.add_parser(
        "import", help="Import folder containing CSV files.")
    parser_one.add_argument("folder_path", type=str, help="Path to folder.")

    # Subparser for action 'exit'
    parser_two = subparsers.add_parser(
        "exit", help="Exit the command line tool.")

    # Subparser for action 'bar'
    parser_three = subparsers.add_parser(
        "bar", help="Plot bar chart of given tags.")
    parser_three.add_argument(
        "tags", nargs="+", help="Tags for the error description.")

    # Subparser for action 'pie'
    parser_four = subparsers.add_parser(
        "pie", help="Plot pie chart of given tags.")
    parser_four.add_argument(
        "tags", nargs="+", help="Tags for the error description.")

    # Subparser for action 'c_bar'
    parser_five = subparsers.add_parser(
        "c_bar", help="Plot bar chart of all tags.")

    # Subparser for action 'c_pie'
    parser_six = subparsers.add_parser(
        "c_pie", help="Plot pie chart of all tags.")

    # Subparser for action 'summary'
    parser_seven = subparsers.add_parser(
        "summary", help="Get the frequency summary description.")

    return parser


def main():
    parser = create_parser()

    print("Interactive CLI Tool.")
    print("Type 'exit' to quit.\nType '--help' for usage information.")

    dh = None
    while True:
        try:
            # Read input command from user
            command = input("\n>>> ").strip()

            # Exit condition
            if command.lower() in {"exit", "quit"}:
                print("Exiting CLI. Goodbye!")
                break

            # Parse the input command
            args = parser.parse_args(shlex.split(command))

            # Call the appropriate function based on the action
            if args.action == "import":
                dh = import_folder(args.folder_path)
                validate_data_handler(dh)
                show_summary(dh)
            elif args.action == "exit":
                exit_cli()
            elif args.action == "bar":
                validate_data_handler(dh)
                plot_bar(args.tags, dh)
            elif args.action == "pie":
                validate_data_handler(dh)
                plot_pie(args.tags, dh)
            elif args.action == "c_bar":
                validate_data_handler(dh)
                plot_complete_bar(dh)
            elif args.action == "c_pie":
                validate_data_handler(dh)
                plot_complete_pie(dh)
            elif args.action == "summary":
                validate_data_handler(dh)
                show_summary(dh)
            else:
                print("Unknown action. Type '--help' for usage information.\n")

        except SystemExit:
            # Catch argparse errors (like missing arguments) and continue the loop
            print("Invalid command. Type '--help' for usage information.\n")
        except Exception as e:
            print(f"An error occurred: {e}\n")


if __name__ == "__main__":
    main()
