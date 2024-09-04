import ollama
import chromadb
import argparse
import docx

# Create an argument parser
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument("-p", "--prompt", type=str, required=True, help="Prompt to generate response for")
parser.add_argument("-m", "--model", type=str, default="llama3.1:latest", help="LLM model to use for generation")
parser.add_argument("-e", "--embedding_model", type=str, default="nomic-embed-text", help="Embedding model to use")
parser.add_argument("-d", "--docx_file", type=str, required=True, help="Path to the DOCX file to be used as document")
args = parser.parse_args()

# Create a ChromaDB client
client = chromadb.Client()

# Create a collection named "test"
collection = client.create_collection(name="test")

# Function to read a docx file and extract its text
def read_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

# Read the docx file
doc_text = read_docx(args.docx_file)

# Split the document text into paragraphs or other chunks as needed
documents = [para for para in doc_text.split('\n') if para.strip() != "" and not para.strip().isdigit()]

# Define the embedding model
embedding_model = args.embedding_model

# Add the documents and embeddings to the collection
for i, d in enumerate(documents):
    response = ollama.embeddings(model=embedding_model, prompt=d)
    embedding = response["embedding"]
    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[d]
    )

# Define the prompt
prompt = args.prompt

# Create embeddings for the prompt
response = ollama.embeddings(
    prompt=prompt,
    model=embedding_model
)

# Query the collection for the most similar document
results = collection.query(
    query_embeddings=[response["embedding"]],
    n_results=1
)

# Get the most similar document
data = results['documents'][0][0]

# Generate a response using the model
output = ollama.generate(
    model=args.model,
    prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
)

# Print the response
print(output['response'])
