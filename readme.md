# Facebook Client

This is a Flask application that serves Virtual legal expert. It utilizes the OpenAI API to create a virtual assistant for legal expertise.

## Prerequisites

Before running the application, make sure you have the following:

- Python 3.x installed
- Flask and other required dependencies installed (see `requirements.txt`)
- OpenAI API key (set it as an environment variable `OPENAI_API_KEY`)

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/RaheesAhmed/DottyBOT.git
   ```

2. Install the dependencies:

   ```shell
   pip install -r requirements.txt
   ```

3. Upload the `knowledgebase.pdf` file to the OpenAI API once the server starts.

## Usage

### create a new `.env` file and add new variable OPENAI_API_KEY

```
OPENAI_API_KEY=ADD YOUR OPENAI API KEY HERE
```

1. Start the Flask server:

```shell
python main.py
```

2. Access the application in your web browser at `http://localhost:5000`.

3. Interact with the virtual assistant by sending messages through the chat interface.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
