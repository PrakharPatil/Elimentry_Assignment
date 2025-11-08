from tensorflow.keras.models import load_model

def load_pd_model():
    model = load_model("app/models/pd_model_nn.h5")
    return model
