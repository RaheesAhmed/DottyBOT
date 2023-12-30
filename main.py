from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import time
from flask_cors import CORS
import os
import dotenv

dotenv.load_dotenv()


app = Flask(__name__)
CORS(app)

api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Upload the PDF file once when the server starts
with open('knowledgebase.pdf', 'rb') as pdf_file:
    file_response = client.files.create(file=pdf_file, purpose='assistants')
file_id = file_response.id

# Create an assistant
assistant_response = client.beta.assistants.create(
    model="gpt-3.5-turbo-1106",
    name="DottyBOT",
    instructions=
    "Benvenuto in DottyBOT, il tuo assistente virtuale esperto legale. come posso aiutarti oggi? Se avete domande su consulenza legale, servizi offerti dal nostro studio, specializzazioni, onorari, nomine, casi di divorzio, tutela di interessi aziendali, incidenti stradali, richieste di asilo o cittadinanza, rappresentanza in tribunale, accuse penali, avvio di un'impresa, controversie contrattuali, infortuni sul lavoro, tutela della proprietà intellettuale, controversie familiari, questioni immobiliari, malasanità, pianificazione successoria, licenziamento senza giusta causa, controversie di lavoro, prodotti difettosi, controversie assicurative, accessibilità, parcheggi, trasporti pubblici, prenotazioni online, modalità di pagamento, consulenza legale online, dati privacy o servizi di traduzione sono qui per aiutarti. Mai e poi mai menzionato il file caricato",
    tools=[{
        "type": "retrieval",
    }],
    file_ids=[file_id])
assistant_id = assistant_response.id




@app.route('/')
def index():
    return render_template('index.html')




@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    print(user_message)
    # Create a thread
    thread_response = client.beta.threads.create()
    thread_id = thread_response.id

    # Send a message to the thread
    client.beta.threads.messages.create(thread_id=thread_id,
                                        role="user",
                                        content=user_message)

    # Execute a run to process the message
    run_response = client.beta.threads.runs.create(thread_id=thread_id,
                                                   assistant_id=assistant_id)

    # Wait for the response
    time.sleep(2)  # Adjust the time as needed

    # Retrieve the final response from the run
    run = client.beta.threads.runs.retrieve(thread_id=thread_id,
                                            run_id=run_response.id)

    # Assuming the run completes, get the latest response from the assistant
    messages_response = client.beta.threads.messages.list(thread_id=thread_id)
    assistant_responses = [
        msg for msg in messages_response.data if msg.role == 'assistant'
    ]
    if assistant_responses:
        latest_response = assistant_responses[-1]
        response = latest_response.content[
            0].text.value if latest_response.content else "No content"
    else:
        response = "No response received."

    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
