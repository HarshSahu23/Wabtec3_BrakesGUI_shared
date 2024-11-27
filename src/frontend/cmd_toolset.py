import argparse
import shlex
import os
import sys

from tabulate import tabulate
from backend.data_handler import DataHandler
from backend.plotter import Plotter

class CommandStructure:
    """
    A class representing the structure of a command in a CLI tool.
    Each command has a name, optional parameters, and help text for both the command and its parameters.
    """

    def __init__(self, cmd_name=None, cmd_help_txt=None, param_name=None, param_help_txt=None, nparams=None):
        """
        Initialize a command structure object.

        Args:
            cmd_name (str): The name of the command (e.g., 'import', 'exit').
            cmd_help_txt (str): The help text describing the command's functionality.
            param_name (str): The name of the parameter for the command, if any (e.g., 'folder_path').
            param_help_txt (str): The help text describing the parameter, if any.
            nparams (str or int): Specifies the number of parameters:
                                  - `None` if no parameters.
                                  - An integer for a fixed number of parameters.
                                  - `'+'` for one or more parameters.
                                  - `'*'` for zero or more parameters.
        """
        self.cmd_name = cmd_name
        self.param_name = param_name
        self.cmd_help_txt = cmd_help_txt
        self.param_help_txt = param_help_txt
        self.nparams = nparams

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

def plot_bar(tags=None, dh: DataHandler = None):
    try:
        filtered_df = dh.ecl_freq_summary[dh.ecl_freq_summary["Description"].isin(
            tags)]
        if filtered_df.empty:
            print(f"No matching tags found for: {tags}")
        else:
            print("Drawing bar chart with given error names...")
            Plotter.plot_bar_chart(
                x=filtered_df["Description"].tolist(),
                y=filtered_df["Frequency"].tolist(),
                xlabel="Description",
                ylabel="Frequency"
            )
    except IndexError:
        print("Please specify tags for the bar chart (e.g., bar_chart tag1 tag2).")


def plot_pie(tags=None, dh: DataHandler = None):
    try:
        filtered_df = dh.ecl_freq_summary[dh.ecl_freq_summary["Description"].isin(
            tags)]
        if filtered_df.empty:
            print(f"No matching tags found for: {tags}")
        else:
            print("Drawing pie chart with given error names...")
            # print(tabulate(filtered_df, headers="keys", tablefmt="grid"))
            Plotter.plot_pie_chart(
                labels=filtered_df["Description"].tolist(),
                data=filtered_df["Frequency"].tolist()
            )
    except IndexError:
        print("Please specify tags for the pie chart (e.g., pie_chart tag1 tag2).")


def plot_complete_bar(dh: DataHandler):
    print("Drawing complete bar chart...")
    Plotter.plot_bar_chart(
        x=dh.ecl_freq_summary["Description"].tolist(),
        y=dh.ecl_freq_summary["Frequency"].tolist(),
        xlabel="Description",
        ylabel="Frequency"
    )


def plot_complete_pie(dh: DataHandler):
    print("Drawing complete pie chart...")
    Plotter.plot_pie_chart(
        labels=dh.ecl_freq_summary["Description"].tolist(),
        data=dh.ecl_freq_summary["Frequency"].tolist()
    )


def validate_data_handler(dh: DataHandler = None):
    if dh == None:
        raise ValueError(
            "The provided data handler object is None. Try importing first.")


def show_summary(dh: DataHandler):
    print("="*20 + "Summary Table" + "="*20)
    print(tabulate(dh.ecl_freq_summary, headers="keys", tablefmt="grid"))


def create_parser():
    """Create the argparse parser with subcommands."""
    parser = argparse.ArgumentParser(
        description="CLI tool for performing actions with options and parameters"
    )

    # Create subparsers for actions
    subparsers = parser.add_subparsers(dest="action", required=True, help="Available actions")

    # This contains all the commands with their respective structure and help texts.
    # Each `CommandStructure` instance defines a command and its attributes.
    commands_desc = [
        CommandStructure("import", "Import folder containing CSV files. Example: import path_to_folder", "folder_path", "Path to the folder contaning CSV files."),
        CommandStructure("exit", "Exit the command line tool."),
        CommandStructure("bar", "Displays a bar chart for specified tags. Example: bar tag1 tag2", "tags", "Tags for the error description.", nparams="+"),
        CommandStructure("pie", "Displays a pie chart for specified tags. Example: pie tag1 tag2", "tags", "Tags for the error description.", nparams="+"),
        CommandStructure("c_bar", "Displays a bar chart for all descriptions and their frequencies."),
        CommandStructure("c_pie", "Displays a pie chart for all descriptions and their frequencies."),
        CommandStructure("summary", "Displays the summary table of descriptions and their frequencies.")
    ]

    # Automatically build subparsers from the commands structure
    # This loop iterates through each `CommandStructure` object in `commands_desc`
    # and generates a subparser with the appropriate parameters and help texts.
    for cmd in commands_desc:
        # Create a subparser for the command, using its name and help text
        tmp_parser = subparsers.add_parser(cmd.cmd_name, help=cmd.cmd_help_txt)

        # If the command has parameters, define them in the subparser
        if cmd.param_name is not None:
            tmp_parser.add_argument(
                cmd.param_name,  # Name of the parameter
                nargs=cmd.nparams,  # Number of arguments for the parameter
                help=cmd.param_help_txt  # Help text describing the parameter
            )

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
                sys.exit(0)
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
