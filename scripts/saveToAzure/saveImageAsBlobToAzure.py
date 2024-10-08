# ----------------------------------------------------------------------------------
# MIT License
#
# Copyright(c) Microsoft Corporation. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# ----------------------------------------------------------------------------------
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



import os
import uuid
import sys
import cv2
from azure.storage.blob import BlockBlobService, PublicAccess

# ---------------------------------------------------------------------------------------------------------
# Method that creates a test file in the 'Sample' folder.
# This sample application creates a test file, uploads the test file to the Blob storage,
# lists the blobs in the container, and downloads the file with a new name.
# ---------------------------------------------------------------------------------------------------------
# Documentation References:
# Associated Article - https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
# What is a Storage Account - http://azure.microsoft.com/en-us/documentation/articles/storage-whatis-account/
# Getting Started with Blobs-https://docs.microsoft.com/en-us/azure/storage/blobs/storage-python-how-to-use-blob-storage
# Blob Service Concepts - http://msdn.microsoft.com/en-us/library/dd179376.aspx
# Blob Service REST API - http://msdn.microsoft.com/en-us/library/dd135733.aspx
# ----------------------------------------------------------------------------------------------------------


def run_sample():
    try:
        # Create the BlockBlobService that is used to call the Blob service for the storage account
        blob_service_client = BlockBlobService(
            account_name='hacklabphantoms', account_key='cOYDn0nxzuzIpg8XRJ0z5WZxZvLuftmO/2B50oJZ2KZd/kyS0QKQd7SQEEueogYfnI/ceat3abWi+AStoIl6MA==')

        # Create a container called 'pictures'.
        container_name = 'pictures'
        blob_service_client.create_container(container_name)

        # Set the permission so the blobs are public.
        blob_service_client.set_container_acl(
            container_name, public_access=PublicAccess.Container)

        #  Get name of user
        name = input("Enter your name: ")

        # Create Sample folder if it not exists, and create a file in folder Sample to test the upload and download.
        local_path = os.path.expanduser("~/AI-pictures")
        if not os.path.exists(local_path):
            os.makedirs(os.path.expanduser("~/AI-pictures"))
        local_file_name = name + ".png"
        full_path_to_file = os.path.join(local_path, local_file_name)

        # load camera
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            # save image with name
            cv2.imshow("Frame", frame)

            # Save image file to folder.
            cv2.imwrite(full_path_to_file, frame)

            print("Temp file = " + full_path_to_file)
            print("\nUploading to Blob storage as blob" + local_file_name)

            # Upload the created file, use local_file_name for the blob name
            blob_service_client.create_blob_from_path(
                container_name, local_file_name, full_path_to_file)

            # List the blobs in the container
            print("\nList blobs in the container")
            generator = blob_service_client.list_blobs(container_name)
            for blob in generator:
                print("\t Blob name: " + blob.name)

            # Download the blob(s).
            # Add '_DOWNLOADED' as prefix to '.txt' so you can see both files in Documents.
            full_path_to_file2 = os.path.join(local_path, str.replace(
                local_file_name ,'.png', '_DOWNLOADED.png'))
            print("\nDownloading blob to " + full_path_to_file2)
            blob_service_client.get_blob_to_path(
                container_name, local_file_name, full_path_to_file2)

            sys.stdout.write("Sample finished running. When you hit <any key>, the sample will be deleted and the sample "
                             "application will exit.")
            sys.stdout.flush()
            input()

            # Clean up resources. This includes the container and the temp files
            # blob_service_client.delete_container(container_name)
            # os.remove(full_path_to_file)
            # os.remove(full_path_to_file2)

            # cap.release()

        cap.release()
        cv2.destroyAllWindows()   

    except Exception as e:
        print(e)


# Main method.
if __name__ == '__main__':
    run_sample()