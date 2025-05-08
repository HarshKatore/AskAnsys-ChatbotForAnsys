# AskAnsys - Chatbot For Ansys

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Ansys](https://img.shields.io/badge/Ansys-2023R1%2B-red)](https://www.ansys.com/)

AskAnsys is an intelligent chatbot designed to assist users with Ansys software queries, troubleshooting, and guidance. Leveraging natural language processing and machine learning, AskAnsys aims to provide instant support for Ansys users across various products in the Ansys suite.

## Features

- **Instant Answers**: Get immediate responses to common Ansys software questions
- **Multi-product Support**: Coverage for Fluent, Mechanical, Discovery, and other Ansys products
- **Tutorial Guidance**: Step-by-step help for completing common tasks
- **Error Troubleshooting**: Solutions for common error messages and issues
- **Best Practices**: Recommendations for simulation setup and workflow optimization
- **Command Assistance**: Help with specific Ansys commands and their parameters
- **Documentation Search**: Quickly find relevant documentation sections

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/HarshKatore/AskAnsys-ChatbotForAnsys.git
cd AskAnsys-ChatbotForAnsys
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure API keys**

Create a `.env` file in the root directory with your API keys:

```
OPENAI_API_KEY=your_openai_api_key
ANSYS_KNOWLEDGE_BASE_API_KEY=your_kb_api_key
```

5. **Run the application**

```bash
python run_app.py
```

## Usage

### Web Interface

After starting the application, navigate to `http://localhost:5000` in your web browser to access the AskAnsys web interface.

### Command Line Interface

For command line usage:

```bash
python cli.py "How do I create a mesh in Ansys Fluent?"
```

### API Integration

AskAnsys can be integrated with other applications using the provided API endpoints:

```python
import requests

response = requests.post('http://localhost:5000/api/ask', 
                        json={'question': 'How do I set up a transient analysis in Mechanical?'})
print(response.json())
```

## Example Queries

- "How do I import CAD geometry into Ansys Mechanical?"
- "What are the best practices for meshing in Fluent?"
- "How can I set up a transient thermal analysis?"
- "What does error code XY-123 mean in Ansys Workbench?"
- "Show me the steps to perform modal analysis"
- "How do I plot von Mises stress in APDL?"
- "What solver settings should I use for my CFD simulation?"

## Development

### Project Structure

```
AskAnsys-ChatbotForAnsys/
├── app/
│   ├── api/           # API endpoints
│   ├── models/        # ML models and data processing
│   ├── static/        # Static web assets
│   ├── templates/     # Frontend templates
│   └── utils/         # Utility functions
├── data/
│   ├── training/      # Training data
│   └── knowledge/     # Knowledge base
├── docs/              # Documentation
├── scripts/           # Utility scripts
├── tests/             # Unit and integration tests
├── .env.example       # Example environment variables
├── requirements.txt   # Dependencies
└── run_app.py         # Application entry point
```

### Contributing

We welcome contributions to AskAnsys! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows our coding standards and includes appropriate tests.

### Adding Knowledge

To expand AskAnsys's knowledge base:

1. Add new training examples to `data/training/`
2. Add product-specific information to `data/knowledge/`
3. Run the knowledge base update script:

```bash
python scripts/update_knowledge_base.py
```

## Future Roadmap

- **Voice Interface**: Add voice recognition and response capabilities
- **Ansys Software Integration**: Direct plugin for Ansys products
- **Advanced Visualization**: Providing visual guidance with images and diagrams
- **User Account System**: Personalized assistance based on user history
- **Multi-language Support**: Expanding beyond English

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions, feature requests, or support, please contact:
- Harsh Katore - harshkatore16@gmail.com

## Acknowledgments

- Ansys, Inc. for providing the software platform and documentation
- OpenAI for natural language processing technologies
- All contributors who have helped improve AskAnsys
