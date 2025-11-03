from germansentiment import SentimentModel

model = SentimentModel()

texts = [
    "Mit keinem guten Ergebniss", "Das ist gar nicht mal so gut",
    "Total awesome!", "nicht so schlecht wie erwartet",
    "Der Test verlief positiv.", "Sie fährt ein grünes Auto."]

result = model.predict_sentiment(texts)
print(result)