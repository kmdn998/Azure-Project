from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import uuid

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]

    try:
        # Get your connection string from an environment variable
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = "imageuploaded"

        blob_name = str(uuid.uuid4())
        blob_client = blob_service_client.get_blob_client(container_name, blob_name)

        # Upload the file
        blob_client.upload_blob(file.read())

        return (
            jsonify({"message": "File uploaded successfully", "blob_name": blob_name}),
            200,
        )
    except Exception as ex:
        print("Exception:")
        print(ex)
        return jsonify({"error": "An error occurred"}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
