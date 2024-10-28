from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk


# Function to locate the pixel to store the password
def locate_password_pixel(image, secret_key, bit_index):
    width, height = image.size
    pixel_index = (bit_index + sum(ord(char) for char in secret_key)) % (width * height)
    return pixel_index % width, pixel_index // width


# Function to encode the password into the image
def encode_password(image_path, password, secret_key, output_path):
    image = Image.open(image_path)
    encoded = image.copy()
    width, height = image.size

    # Convert password to binary
    password_bits = ''.join(format(ord(c), '08b') for c in password)
    print(f"Password binary: {password_bits}")  # Debugging statement

    # Iterate over password bits and modify the pixel data
    bit_index = 0
    for i in range(len(password_bits)):
        x, y = locate_password_pixel(image, secret_key, bit_index)  # Get pixel for this bit
        pixel_data = list(encoded.getpixel((x, y)))

        # Modify the least significant bit of the pixel
        pixel_data[0] = (pixel_data[0] & ~1) | int(password_bits[i])  # Modify red channel
        encoded.putpixel((x, y), tuple(pixel_data))

        bit_index += 1
        if bit_index >= len(password_bits):
            break

    # Save the encoded image
    encoded.save(output_path)
    return output_path


# Function to decode the password from the image
def decode_password(image_path, secret_key, password_length):
    image = Image.open(image_path)
    password_bits = ""

    # Loop through expected bits (8 bits per character)
    for i in range(password_length * 8):
        x, y = locate_password_pixel(image, secret_key, i)  # Get pixel for this bit
        pixel_data = image.getpixel((x, y))

        # Extract the least significant bit from the red channel
        password_bits += str(pixel_data[0] & 1)

    # Convert binary bits back to characters
    password = ""
    for i in range(0, len(password_bits), 8):
        byte = password_bits[i:i + 8]
        if len(byte) < 8:
            break
        password += chr(int(byte, 2))

    return password.rstrip('\x00')


# GUI Setup
root = Tk()
root.title("Steganography Password Encoder/Decoder")

# Create a Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Tab for Encoding
encode_tab = Frame(notebook)
notebook.add(encode_tab, text="Encode Password")

# Tab for Decoding
decode_tab = Frame(notebook)
notebook.add(decode_tab, text="Decode Password")

# Global variable to store the image path
image_path = None
encoded_image_path = None


# Function to upload an image for encoding
def upload_image_for_encoding():
    global image_path, img_display
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

    if image_path:
        img = Image.open(image_path)
        img.thumbnail((300, 300))  # Resize image for display
        img_display = ImageTk.PhotoImage(img)

        # Update the label to show the image
        image_label.config(image=img_display)
        image_label.image = img_display  # Keep a reference to avoid garbage collection
        image_label.pack()


# Function to upload an encoded image for decoding
def upload_image_for_decoding():
    global encoded_image_path, decoded_img_display
    encoded_image_path = filedialog.askopenfilename(title="Select Encoded Image", filetypes=[("Image Files", "*.png")])

    if encoded_image_path:
        img = Image.open(encoded_image_path)
        img.thumbnail((300, 300))  # Resize image for display
        decoded_img_display = ImageTk.PhotoImage(img)

        # Update the label to show the encoded image
        decoded_image_label.config(image=decoded_img_display)
        decoded_image_label.image = decoded_img_display  # Keep a reference to avoid garbage collection
        decoded_image_label.pack()


# UI Components for Encoding
upload_button = Button(encode_tab, text="Upload Image", command=upload_image_for_encoding)
upload_button.pack()

image_label = Label(encode_tab)
image_label.pack()

# Password Entry
password_label = Label(encode_tab, text="Enter Password:")
password_label.pack()
password_entry = Entry(encode_tab)
password_entry.pack()

# Secret Key Entry
key_label = Label(encode_tab, text="Enter Secret Key:")
key_label.pack()
key_entry = Entry(encode_tab)
key_entry.pack()

# Encode Button
encode_button = Button(encode_tab, text="Encode Password", command=lambda: encode_button_click())
encode_button.pack()


def encode_button_click():
    if not image_path or not password_entry.get() or not key_entry.get():
        messagebox.showwarning("Input Error", "Please provide an image, a password, and a secret key.")
        return

    try:
        output_path = filedialog.asksaveasfilename(defaultextension=".png", title="Save Encoded Image",
                                                   filetypes=[("PNG files", "*.png")])
        if output_path:
            encode_password(image_path, password_entry.get(), key_entry.get(), output_path)
            messagebox.showinfo("Success", "Password encoded successfully!")

            # Clear the fields after encoding
            image_label.config(image=None)
            password_entry.delete(0, END)
            key_entry.delete(0, END)
    except Exception as e:
        messagebox.showerror("Error", str(e))


# UI Components for Decoding
upload_decode_button = Button(decode_tab, text="Upload Encoded Image", command=upload_image_for_decoding)
upload_decode_button.pack()

decoded_image_label = Label(decode_tab)
decoded_image_label.pack()

# Secret Key Entry for Decoding
key_label_decode = Label(decode_tab, text="Enter Secret Key:")
key_label_decode.pack()
key_entry_decode = Entry(decode_tab)
key_entry_decode.pack()

length_label = Label(decode_tab, text="Enter expected password length:")
length_label.pack()
length_entry = Entry(decode_tab)
length_entry.pack()

# Decode Button
decode_button = Button(decode_tab, text="Decode Password", command=lambda: decode_button_click())
decode_button.pack()

# Decoded Password Display
decoded_label = Label(decode_tab, text="Decoded Password: ")
decoded_label.pack()


def decode_button_click():
    if not encoded_image_path or not key_entry_decode.get() or not length_entry.get():
        messagebox.showwarning("Input Error", "Please provide an encoded image, a secret key, and a password length.")
        return

    try:
        password_length = int(length_entry.get())
        decoded_password = decode_password(encoded_image_path, key_entry_decode.get(), password_length)

        if decoded_password:
            decoded_label.config(text=f"Decoded Password: '{decoded_password}'")
        else:
            decoded_label.config(text="No password found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


root.mainloop()
