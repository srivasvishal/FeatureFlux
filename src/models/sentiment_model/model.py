from transformers import pipeline

# Load pre-trained sentiment-analysis pipeline
model = pipeline("sentiment-analysis")

def predict_sentiment(text):
    return model(text)

if __name__ == "__main__":
    with open('sample_input.txt', 'r') as file:
        input_text = file.read()
    print(predict_sentiment(input_text))