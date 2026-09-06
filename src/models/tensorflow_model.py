import tensorflow as tf


class IncidentClassifierTF:
    def __init__(self):
        self.categories=["Fire", "Traffic Accident", "Power Outage", "Medical Emergency", "Infrastructure Failure"]
        self.severities=["Low", "Medium", "High", "Critical"]

    def classify_incident(self,text:str)->dict:
        input_tensor=tf.constant([text])
        tf.random.set_seed(len(text))
        type_probs=tf.random.uniform(shape=[len(self.categories)])
        severity_probs=tf.random.uniform(shape=[len(self.severities)])
        type_idx=tf.argmax(type_probs).numpy()
        severity_idx=tf.argmax(severity_probs).numpy()
        data_used={
            "input tensor shape":str(input_tensor.shape),
            "type probabilities":type_probs.numpy().tolist(),
            "severity probabilities":severity_probs.numpy().tolist()
        }
        return {
            "category":self.categories[type_idx],
            "severity":self.severities[severity_idx],
            "tf data context":data_used
        }
