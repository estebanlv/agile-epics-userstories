# Agile Epics to User Stories Generator

## Overview

The Agile Epics to User Stories Generator is a web application designed to help Agile teams break down epics into detailed user stories. This tool leverages OpenAI's language model to generate user stories based on a provided epic description, making it easier for teams to manage their work and ensure clarity in their project requirements.

## Features

- **Epic to User Stories Generation**: Input an epic description and receive a set of user stories with detailed descriptions and effort points.
- **User Story Extension**: Extend existing user stories with additional details, subtasks, acceptance criteria, and definitions of done.
- **Responsive Design**: The application is designed to work on desktop.
- **User-Friendly Interface**: Simple and intuitive interface for easy navigation and usage.

## Technologies Used

- **Backend**: Python, FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **Database**: Not applicable (data is processed in-memory)
- **OpenAI API**: For generating user stories and extending them
- **Pydantic**: For data validation

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/agile-epics-userstories.git
   cd agile-epics-userstories
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   - Create a `.env` file in the root directory and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

5. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

6. Open your browser and navigate to `http://127.0.0.1:8000` to access the application.

## Usage

1. Enter your epic description in the provided textarea.
2. Click on "Generate User Stories" to see the generated user stories.
3. You can extend any user story by clicking the "Extend Story" button, which will provide additional details.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.