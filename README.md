# Language Learner

Language Learner is a web-app designed to help users learn from books using multimedia resources. Traditional methods of language learning often involve reading books, but studies have shown that incorporating multimedia can enhance the learning process, particularly for listening and conversation skills.

## Description

The Language Learner app aims to provide a comprehensive and interactive language learning experience. By turning book content into multimedia resources, it offers users an efficient way to improve their language skills. The app generates conversations and immersive pictures with captions in different languages, allowing users to practice listening, reading, and conversation skills in a dynamic and engaging manner. Additionally, users can view conversations from other learners and customize their own listening tests.

## Features

- Transform book content into multimedia resources for improved learning efficiency.
- Generate conversations and immersive pictures with captions in different languages.
- View conversations from other learners for additional practice and inspiration.
- Customize listening tests to focus on specific language skills.
- User-friendly interface for easy navigation and access to learning resources.

## Installation and Setup

### Backend Setup and Configuration

1. Apply for Google Cloud credentials for the translation function. Refer to the documentation and apply for credentials at [Google Cloud Credentials](https://developers.google.com/workspace/guides/create-credentials).

2. Obtain the OpenAI GPT API key from the [OpenAI platform](https://platform.openai.com/api-keys).

3. Set up the PostgreSQL database by following the necessary steps and configuration.

4. Install the required Python packages by running the following command:
pip install -r server/requirements.txt

5. Configure the relevant environment variables. Create a `var.sh` file and write the following lines:
export OPENAI_API_KEY="apikey" export GOOGLE_APPLICATION_CREDENTIALS="credential"

Note: Replace "apikey" with your actual OpenAI GPT API key and "credential" with the path to your Google Cloud credentials file.

Then, run the following command to load the environment variables:
source var.sh

6. Start the server by running the following command:
python main.py

### Frontend Setup and Configuration

1. Create a `.env` file in the `frontend` directory and configure the `VUE_APP_API_BASE_URL` variable. For local development, you can set it to `http://localhost:5000` to match the backend server URL.

2. Install the necessary Node modules by running the following command within the `frontend` directory:
npm install

3. Start the Vue project as the frontend by running the following command within the `frontend` directory:
npm run serve

## Tech Stack

The Language Learner app is built using the following technologies:

- Backend: Flask framework with Python 3.9.
- Frontend: Vue.js with Bootstrap-Vue (Bootswatch) for UI components.
- Database: PostgreSQL for storing user data.

## Contributions

Contributions are always welcome! If you find any bugs or have suggestions for new features, please feel free to open an issue or submit a pull request.

## License

This is a personal project, and no licenses are needed for reuse.

Note: Make sure to keep the necessary credentials and sensitive information secure.

If you have any further questions or issues, please don't hesitate to contact me (wentungwen@gmail.com)!