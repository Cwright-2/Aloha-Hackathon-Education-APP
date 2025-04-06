from google.cloud import aiplatform
import base64
import json

# Initialize Vertex AI
aiplatform.init(
    project="alohadata-team10",  #project id
    location="us-central1"   # ai model region
)

def classify_cloud_image(image_path):
    #load end point
    endpoint_list = aiplatform.Endpoint.list(filter='display_name="skyquest_endpoint"')
    if not endpoint_list:
        return "Error: Endpoint not found."

    endpoint = endpoint_list[0]

    # Read and encode the image
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # create instance
    instance = {
        "content": encoded_image
    }

    #send prediction request
    prediction = endpoint.predict(instances=[instance])

    #checks if prediction is valid
    if prediction and prediction.predictions:
        predictions = prediction.predictions[0]
        labels = predictions['displayNames']
        confidences = predictions['confidences']
        
        # find highest confidence rating
        max_confidence_idx = confidences.index(max(confidences))
        return labels[max_confidence_idx]
    else:
        return "Error: No prediction returned."
