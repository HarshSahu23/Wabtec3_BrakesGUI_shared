# Error Analyzer 📊

<a href="https://www.wabteccorp.com/" target="_blank">
  <img src="https://www.wabteccorp.com/themes/custom/wabtec/images/Wabtec-logo-White.svg" alt="Wabtec" width="200" height="100"/>
</a>
<p></p>

> A Python-based application for analyzing error codes from CSV files with interactive visualizations.

## Features ✨

- Interactive GUI built with PyQt5
- Real-time error code analysis
- Dynamic visualization using matplotlib
- CSV file processing and management
- Comprehensive error frequency reporting

## Installation 🚀

### Prerequisites

- Python 3.8+
- Git

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared.git
cd Wabtec3_BrakesGUI_shared
```

2. Set up virtual environment:
```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Unix/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure 📁

```
.
├── assets                  # Contains App screenshots for documentation.
├── build                   # Contains intermediate build files generated by pyinstaller.
│                             This is not present in repo but will be created during build.
│                             Don't commit this folder.
├── build_scripts           # Contains build scripts.
│   ├── build_exe.py        # Contains code to generate exe.
│   ├── exclude_modules.py  # Conatins modules to be excluded during build to reduce build size.
│   └── main.spec           # Contains specifications that can be used pyinstaller.
├── csv                     # Containes CSV files for testing purposes.
├── dist                    # Contains final build files generated by pyinstaller.
│                             This is not present in repo but will be created during build.
│                             Don't commit this folder. 
├── exploratory             # Containes jupyter notebook for exploratory analysis.
│   └── explore.ipynb       # Used to develop functions early on. 
├── instructions.md         # Some common instructions on naming conventions and building exe.
├── readme.md               # Containes readme instructions.
├── requirements.txt        # Containes requirements needed to be installed before start working. 
└── src                     # Containes main source code.
    ├── backend                     # Backend code for data processing.
    │   ├── data_handler.py         # Main class that exposes functionality to frontend.
    │   ├── data_processors         # Containes files for main data processing.
    │   │   ├── dmp_processor.py    # DMP error log Processor.
    │   │   ├── ecf_processor.py    # Error code frequency Processor. 
    │   │   └── ecl_processor.py    # Error code listing Processor.
    │   ├── plotter.py              # Plotting functions.
    │   └── utils                   # Important untility code.
    │       ├── exceptions.py       # Containes custom exceptions code. 
    │       ├── file_classifier.py  # Containes file classification code to 
    │       │                         identify what type of CSV file we are reading currently.  
    │       ├── file_types.py       # Containes custom exceptions code. 
    │       ├── folder_validator.py # Containes custom exceptions code.
    │       └── logging_config.py   # Containes custom exceptions code. 
    ├── frontend                    # Contained frontend code.
    │   ├── cmd_toolset.py          # Code for CLI.
    │   └── gui.py                  # Code for GUI.
    ├── main.py                     # Main entry point.
    └── tester.ipynb                # Jupyter notebook to test backend functions.

```

## Usage 💡

1. Launch the application:
```bash
python main.py
```

2. Process error logs:
   - Place CSV files in the `csv/` directory
   - Input expected error descriptions
   - View analysis results and visualizations

OR 

## Use the GUI 💻
  <br/>

  ### A) Browse Files to upload :
  <p align="left">
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S1.png" alt="Screenshot 1" width="400" height="250"/>
  </p>

  ### B) Select files to upload :
  <p align="left">
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S2.png" alt="Screenshot 2" width="400" height="250"/>
  </p>

  ### C) Select/Search various errors
  <p align="left">
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S3.png" alt="Screenshot 3" width="400" height="250"/>
  </p>
  
  ### D) Use dashboard to view charts & interact with them:
  <p align="left">
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S4.png" alt="Screenshot 4" width="400" height="250"/>
  </p>

  ### E) View various charts:
  <p align="left">
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S5.png" alt="Screenshot 5" width="400" height="250" style="display: inline-block; margin-right: 10px;"/>
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S5_1.png" alt="Screenshot 5_1" width="400" height="250" style="display: inline-block; margin-right: 10px;"/>
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S5_2.png" alt="Screenshot 5_2" width="400" height="250" style="display: inline-block; margin-right: 10px;"/>
  </p>

  ### F) Get Detailed Data of any selected errors, apply filters
   <p align="left">
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S6.png" alt="Screenshot 6" width="400" height="250" style="display: inline-block; margin-right: 10px;"/>
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S7.png" alt="Screenshot 7" width="400" height="250" style="display: inline-block; margin-right: 10px;"/>
  </p>

  ### G) View Dump Log
  <p align="left">
  <img src = "https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/81aaa1ab2971562c79e1c544864f95dd936e187b/assets/S8.png" alt="screenshot 8" width="400" height="250">
  </p>

  ### H) Detailed Data for Dump Files
  <p align="left">
  <img src = "https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/81aaa1ab2971562c79e1c544864f95dd936e187b/assets/S9.png" alt="screenshot 9" width="400" height="250">
  </p>


## Development 🛠️

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use descriptive variable and function names
- Include docstrings and comments where appropriate

### Testing

```bash
# Run tests
python -m pytest tests/

# Check code coverage
python -m pytest --cov=src tests/
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/amazing-feature
```

3. Commit your changes:
```bash
git commit -m 'Add amazing feature'
```

4. Push to your branch:
```bash
git push origin feature/amazing-feature
```

5. Open a Pull Request

### Contribution Guidelines

- Write clear commit messages
- Include tests for new features
- Update documentation as needed
- Submit PRs to the `develop` branch

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Made with ❤️ by Team ^_^ - Exceed 3.0
</div>
