# Development Branch
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
├── assets                                          # App/Repo related assets here.
├── build_scripts                                   # Folder for Build related scripts.    
│   ├── build_exe.py                                    -> Script to generate exec.            
│   ├── exclude_modules.py                              -> List of modules to be excluded.                
│   └── main.spec                                       -> Specifications that can be used with pyinstaller.        
├── csv                                             # CSV files for testing purposes. 
├── instructions.md                                 # Contains general instructions about project (to be merged with README).        
├── readme.md                                       # Project instructions.
├── requirements.txt                                # Required Python packages list.            
└── src                                             # Containes the source code.   
    ├── backend                                         -> Code for backend and data processing.    
    │   ├── data_extractor                                  ->> Code for Data extraction.        
    │   │   ├── dataframe_classifier.py                         - Identifies the type of log being processed.                                
    │   │   └── dataframe_extractor.py                          - Extracts the CSV data as a dataframe.
    │   ├── data_handler.py                                 ->> Code common interface that exposes all the backend functionality to frontend. 
    │   ├── data_processors                                 ->> Code for analytical processing and data formatting.
    │   │   ├── detailed_data_for_error_grouper.py              - Generate custom dataframe table to obtain detailed data.
    │   │   ├── dmp_processor.py                                - Dump file procesing and formatting.
    │   │   ├── ecl_processor.py                                - Error log processor.
    │   │   ├── error_grouper_for_error_log_tab.py              - Error group generator for error log tab in UI.
    │   │   └── table_maker_for_summary_tab.py                  - Table maker for summary tab in UI.
    │   ├── json_config_loader.py                           ->> Loads JSON config from the directory.
    │   ├── plotter.py                                      ->> Plotting functions for the use in CLI.
    │   └── utils                                           ->> Utility code.
    │       ├── exceptions.py                                   - Custom exception class code.
    │       ├── folder_validator.py                             - Folder path validator.
    │       └── logging_config.py                               - Logging config file.
    ├── backup_config.json                              -> Backup config JSON in case some corruption of original happens.
    ├── config.json                                     -> Config file for the app.
    ├── frontend                                        -> Frontend code Part.
    │   ├── cmd_toolset.py                                  ->> Code for cmd toolset.
    │   ├── compute                                         ->> Computes various charting elements.
    │   │   ├── calculate_percentages.py                        - Annotaions on the chart.
    │   │   ├── summary_viz.py                                  - Chart for the summary tab.
    │   │   ├── update_chart.py                                 - Updates chart when specific button clicked in error log tab.
    │   │   └── visualizations.py                               - Charts for the error log tab.
    │   ├── gui.py                                          ->> Main GUI entrypoint.
    │   ├── tabs                                            ->> Contains GUI code for different tabs.                                      
    │   └── utils                                           ->> Utility functions for various widgets.    
    │       ├── create_tab_labels.py                            - CSS designs for labeling.
    │       ├── css_utils.py                                    - CSS designs for error log tab.
    │       ├── edit_folder_metadata.py                         - Widget for editing Coach and depot data
    │       ├── render_section_header.py                        - CSS for section header.
    │       ├── render_sidebar.py                               - Display custom sidebar.
    │       └── sidebar_utils.py                                - Widgets displayed inside sidebar. 
    ├── main.py                                         -> Main entry code for the app.
    └── tester.ipynb                                    -> Tester python notebook to test the new functions. 
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
  <p>
    <a href="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/raw/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S1.png">
      <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/raw/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S1.png" alt="Screenshot 1" height="250" width="400" style="object-fit: cover;"/>
    </a>
  </p>

  ### B) Select files to upload :
  <p align="left">
    <a href="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S2.png">
      <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S2.png" alt="Screenshot 2" height="250" width="400" style="object-fit: cover;"/>
    </a>
  </p>

  ### C) Select/Search various errors
  <p align="left">
    <a href="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S3.png"><img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S3.png" height="250" width="400" style="object-fit: cover;" alt="Screenshot 3" width="400" height="250"/></a>
  </p>
  
  ### D) Use dashboard to view charts & interact with them:
  <p align="left">
    <a href="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S4.png"><img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S4.png" height="250" width="400" style="object-fit: cover;" alt="Screenshot 4" width="400" height="250"/></a>
  </p>

  ### E) View various charts:
  <p align="left">
    <a href="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S5.png">
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S5.png" alt="Screenshot 5" width="400" height="250" style="display: inline-block; margin-right: 10px;"/></a>
    <a href="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S5_1.png">
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S5_1.png" alt="Screenshot 5_1" width="400" height="250" style="display: inline-block; margin-right: 10px;"/></a>
    <a href="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S5_2.png">
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S5_2.png" alt="Screenshot 5_2" width="400" height="250" style="display: inline-block; margin-right: 10px;"/></a>
  </p>

  ### F) Get Detailed Data of any selected errors, apply filters
   <p align="left">
    <a href = "https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S6.png"><img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S6.png" alt="Screenshot 6" width="400" height="250" style="display: inline-block; margin-right: 10px;"/></a>
    <a href="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S7.png"><img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/89d6f4d39e1d1ce385356e2394db8c27d39bfda4/assets/S7.png" alt="Screenshot 7" width="400" height="250" style="display: inline-block; margin-right: 10px;"/></a>
  </p>

  ### G) View Dump Log
  <p align="left">
  <a href="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/81aaa1ab2971562c79e1c544864f95dd936e187b/assets/S8.png">
  <img src = "https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/81aaa1ab2971562c79e1c544864f95dd936e187b/assets/S8.png" alt="screenshot 8" width="400" height="250"></a>
  </p>

  ### H) Detailed Data for Dump Files
  <p align="left">
  <a href="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/81aaa1ab2971562c79e1c544864f95dd936e187b/assets/S9.png"><img src = "https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/81aaa1ab2971562c79e1c544864f95dd936e187b/assets/S9.png" alt="screenshot 9" width="400" height="250"></a>
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
