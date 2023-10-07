import streamlit as st
import os
def main():
    st.title("File Upload Example")
    
    uploaded_file = st.file_uploader("Choose a file...", type=["jpg", "png", "txt", "csv", "pdf"])
    
    if uploaded_file is not None:
        unique_filename = os.path.join("files", uploaded_file.name)

        # Save the uploaded file to the specified directory
        with open(unique_filename, "wb") as f:
            f.write(uploaded_file.read())
        st.success("File uploaded successfully!")

if __name__ == "__main__":
    main()
