# pixelLock

Steganography Password Encoder/Decoder
Overview
This project is a Python application that enables users to encode passwords into images using steganography techniques and decode them later. The application provides a graphical user interface (GUI) for easy interaction, allowing users to upload images, enter passwords, and manage secret keys for secure encoding and decoding.

Features
Encode Passwords: Hide a password in a single pixel of an image while leaving the rest of the image unchanged.
Decode Passwords: Retrieve the hidden password from the encoded image using a secret key.
User-Friendly GUI: Easy-to-use interface for uploading images and entering passwords and keys.
Image Preview: Display the original and encoded images within the application.
Technologies Used
Python
Tkinter (for GUI)
Pillow (PIL) for image processing

Installation
To run this project, you'll need Python installed on your machine. Follow these steps to set up the project:

Clone the repository

Navigate to the project directory: cd steganography-password-encoder-decoder

Install the required packages: pip install pillow

Run the application: python steganography.py

Usage
Encoding a Password:
Navigate to the "Encode Password" tab.
Click "Upload Image" to select an image file.
Enter the password you want to encode.
Provide a secret key for encoding.
Click "Encode Password" to save the encoded image.
Example:
<img width="460" alt="encode_pass_pic" src="https://github.com/user-attachments/assets/c46a4894-4981-4073-bb55-d2293847690d">


Decoding a Password:
Switch to the "Decode Password" tab.
Click "Upload Encoded Image" to select the encoded image file.
Enter the secret key used for encoding.
Specify the expected password length.
Click "Decode Password" to retrieve the hidden password.
Example: 
<img width="460" alt="decode_pass_pic" src="https://github.com/user-attachments/assets/1419a9ed-53ae-4b9e-84d7-de17f6785c08">


Contributing
Contributions are welcome! If you have suggestions for improvements or features, please create an issue or submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Pillow Documentation: https://pillow.readthedocs.io/en/stable/
Tkinter Documentation: https://docs.python.org/3/library/tkinter.html
