# Error Analyzer 📊

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
git clone https://github.com/yourusername/error-analyzer.git
cd error-analyzer
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
ErrorAnalyzer/
├── csv/                  # Error log CSV files
├── data/                 # Testing data repository
├── src/
│   ├── backend/         # Core analysis logic
│   └── frontend/        # PyQt5 GUI implementation
├── main.py              # Application entry point
├── requirements.txt     # Dependencies
└── setup.py            # Package configuration
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
Made with ❤️ by the Error Analyzer Team
</div>