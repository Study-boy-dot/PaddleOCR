import ollama
import chromadb
import argparse
import docx
import fnmatch
import os

# Create an argument parser
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument("-p", "--prompt", type=str, required=True, help="Prompt to generate response for")
parser.add_argument("-m", "--model", type=str, default="llama3.1:latest", help="LLM model to use for generation")
parser.add_argument("-e", "--embedding_model", type=str, default="nomic-embed-text", help="Embedding model to use")
parser.add_argument("-f", "--file", type=str, help="Path to a single DOCX file to be processed")
parser.add_argument("--pattern", type=str, help="Pattern to filter DOCX files (e.g., '*improve*')")
parser.add_argument("--dir", type=str, help="Directory containing the DOCX files")
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

documents = []

# Process files based on input
if args.dir:
	# Use fnmatch to match files in the directory based on the pattern
	for file_name in os.listdir(args.dir):
		if args.pattern and fnmatch.fnmatch(file_name, args.pattern) and file_name.endswith(".docx"):
			file_path = os.path.join(args.dir, file_name)
			doc_text = read_docx(file_path)
			documents.extend([para for para in doc_text.split('\n') if para.strip() != "" and not para.strip().isdigit()])
		elif not args.pattern and file_name.endswith(".docx"):
			file_path = os.path.join(args.dir, file_name)
			doc_text = read_docx(file_path)
			documents.extend([para for para in doc_text.split('\n') if para.strip() != "" and not para.strip().isdigit()])
elif args.file:
	# Process a single DOCX file
	doc_text = read_docx(args.file)
	documents = [para for para in doc_text.split('\n') if para.strip() != "" and not para.strip().isdigit()]
else:
	raise ValueError("You must provide either --file or both --dir and --pattern")

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
