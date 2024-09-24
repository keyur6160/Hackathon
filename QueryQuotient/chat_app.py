import streamlit as st
import PyPDF2
import docx
from io import BytesIO

# Function to read .txt files
def read_txt(file):
    return file.read().decode("utf-8")

# Function to read .pdf files
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text() or ''
    return text

# Function to read .docx files (if needed in future)
def read_docx(file):
    doc = docx.Document(BytesIO(file.read()))  # Read file into memory as binary
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

# Main app
st.title("Chat Question and Answer App")

# Create a dictionary to store clusters
if 'clusters' not in st.session_state:
    st.session_state.clusters = {}
if 'current_cluster' not in st.session_state:
    st.session_state.current_cluster = None

# Tab layout
tab1, tab2 = st.tabs(["Upload Files", "Ask a Question"])

# Allowed file types
ALLOWED_FILE_TYPES = ["txt", "pdf"]

# Tab 1: Upload Files
with tab1:
    st.subheader("Create a Cluster and Upload Files")
    
    cluster_name = st.text_input("Enter Cluster Name:")
    
    uploaded_files = st.file_uploader("Upload your text and PDF files (.txt, .pdf)", type=["txt", "pdf"], accept_multiple_files=True)

    if st.button("Upload to Cluster"):
        if cluster_name and uploaded_files:
            if cluster_name not in st.session_state.clusters:
                st.session_state.clusters[cluster_name] = {}

            invalid_files = []
            for uploaded_file in uploaded_files:
                # Check for invalid file types
                file_extension = uploaded_file.name.split(".")[-1].lower()
                if file_extension not in ALLOWED_FILE_TYPES:
                    invalid_files.append(uploaded_file.name)
                else:
                    # Valid file processing
                    if uploaded_file.type == "text/plain":
                        st.session_state.clusters[cluster_name][uploaded_file.name] = read_txt(uploaded_file)
                    elif uploaded_file.type == "application/pdf":
                        st.session_state.clusters[cluster_name][uploaded_file.name] = read_pdf(uploaded_file)
            
            # If there are any invalid files, do not save the cluster
            if invalid_files:
                st.warning(f"The following files have unsupported extensions: {', '.join(invalid_files)}. Please remove them and try again.")
            else:
                st.session_state.current_cluster = cluster_name  # Keep track of the current cluster
                st.success(f"Files uploaded successfully to cluster '{cluster_name}'!")
        else:
            st.warning("Please enter a cluster name and upload files.")

    # Clear Button
    if st.button("Clear Current Cluster"):
        if st.session_state.current_cluster:
            del st.session_state.clusters[st.session_state.current_cluster]
            st.session_state.current_cluster = None
            st.success("Current cluster has been cleared. You can create a new one.")
        else:
            st.warning("No current cluster to clear.")

# Tab 2: Ask a Question
with tab2:
    st.subheader("Select a Cluster and Ask a Question")
    
    cluster_names = list(st.session_state.clusters.keys())
    
    selected_cluster = st.selectbox("Select a Cluster:", cluster_names)

    user_question = st.text_input("Enter your question:")
    
    if st.button("Get Answer"):
        if selected_cluster and user_question:
            documents = st.session_state.clusters[selected_cluster]
            response = "This is a placeholder response. Implement your own logic to answer questions based on the documents."
            st.write(response)
        else:
            st.warning("Please select a cluster and enter a question.")
