# Voice Notes App

The Voice Notes App is a web-based application that allows users to upload audio files, transcribe them to text, and generate summaries from the transcriptions. It utilizes machine learning models for both speech-to-text conversion and text summarization. The app integrates with Firebase to store the transcriptions and summaries.

## Features

- Audio File Upload: Upload an audio file in WAV format.
- Speech-to-Text Conversion: Converts the audio into text using Whisper.
- Text Summarization: Generates a summary of the transcription using the **T5** summarization model.
- Firebase Integration: Stores transcriptions and summaries in Firebase Firestore for future retrieval.
- User Interface: Built with Streamlit for easy interaction and visualization.

## Tech Stack

- Frontend: Streamlit
- Backend: Python
- Machine Learning:
 - Speech-to-Text: Whisper by OpenAI
 - Summarization: T5 (Text-to-Text Transfer Transformer)
- Database: Firebase Firestore
- Authentication: Firebase Authentication
- Deployment: Streamlit Cloud or any other cloud platform

## Installation

### Prerequisites:

- Python 3.x
- pip package manager
- Git (optional, if you want to clone the repository)

### Steps to Install:

1. Clone the repository:
    ```bash
    git clone https://github.com/mehtaharshit99/voice-notes-app.git
    cd voice-notes-app
2. Set up a virtual environment:
    python3 -m venv venv
    source venv/bin/activate
3. Install the dependencies:
    pip install -r requirements.txt
4. Firebase Setup:
    Create a Firebase project and set up Firestore and Authentication.
    Download the Firebase Admin SDK credentials and store the credentials file in your project folder or set them up in your environment.
5. Run the application:
    streamlit run app.py


## Code Explanation:
### app.py:
This is the main Streamlit file where the UI components are implemented. It handles:
- File uploads
- Speech-to-text processing
- Summarization
- Displaying results
- Storing results in Firebase

### model/summarizer.py:
This file contains code for loading and using the T5 model to generate summaries of transcribed text. The T5 model is loaded using the Hugging Face transformers library.

### model/whisper.py:
This file handles the transcription of audio using Whisper. The audio is processed and converted into text for summarization.

## Challenges Faced:
- Model Limitations: The initial summarization model provided summaries that often did not meet expectations. Alternatives like T5 were tested to improve results.
- Audio File Size: Handling larger audio files and ensuring they are uploaded without hitting Streamlit or Firebase limits was a challenge.
- Caching and Optimization: Efficient caching was implemented to ensure that the models (Whisper and T5) loaded quickly and did not affect performance.

## Future Improvements:
- Enhanced Summarization Models: Experiment with alternative models like Pegasus for improved summaries.
- Multilingual Support: Extend the app to support multiple languages for transcription and summarization.
- Additional Features: Implement sentiment analysis or topic modeling on the transcriptions to extract further insights.

## Acknowledgments:
- Hugging Face for providing the pre-trained T5 model and the transformers library.
- OpenAI for their Whisper model for transcription.
- Firebase for providing cloud storage and authentication services.
    

