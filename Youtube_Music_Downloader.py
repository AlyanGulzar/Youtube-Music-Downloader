import os
from tkinter import Tk, Label, Button, Entry, StringVar, filedialog, messagebox
from pytube import YouTube, Playlist
from moviepy.editor import VideoFileClip


class YTDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("500x300")
        self.root.configure(bg="#F0F0F0")

        # URL Entry
        self.url_label = Label(root, text="YouTube URL:", bg="#F0F0F0", font=("Arial", 12))
        self.url_label.pack(pady=10)
        self.url_var = StringVar()
        self.url_entry = Entry(root, textvariable=self.url_var, width=50)
        self.url_entry.pack(pady=5)

        # Destination Folder
        self.dest_label = Label(root, text="Destination Folder:", bg="#F0F0F0", font=("Arial", 12))
        self.dest_label.pack(pady=10)
        self.dest_var = StringVar()
        self.dest_entry = Entry(root, textvariable=self.dest_var, width=50)
        self.dest_entry.pack(pady=5)
        self.browse_button = Button(root, text="Browse", command=self.browse_folder, bg="#008CBA", fg="white")
        self.browse_button.pack(pady=5)

        # Download Buttons
        self.download_mp4_button = Button(root, text="Download MP4", command=self.download_mp4, bg="#28A745", fg="white")
        self.download_mp4_button.pack(pady=5)

        self.download_mp3_button = Button(root, text="Download MP3", command=self.download_mp3, bg="#28A745", fg="white")
        self.download_mp3_button.pack(pady=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        self.dest_var.set(folder)

    def download_mp4(self):
        url = self.url_var.get()
        destination = self.dest_var.get()
        if not url or not destination:
            messagebox.showerror("Error", "Please provide a valid URL and destination folder.")
            return

        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            messagebox.showinfo("Downloading", f"Downloading {yt.title}...")
            stream.download(output_path=destination)
            messagebox.showinfo("Success", "Download completed!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download video: {e}")

    def download_mp3(self):
        url = self.url_var.get()
        destination = self.dest_var.get()
        if not url or not destination:
            messagebox.showerror("Error", "Please provide a valid URL and destination folder.")
            return

        try:
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            messagebox.showinfo("Downloading", f"Downloading {yt.title}...")
            audio_path = stream.download(output_path=destination)

            # Convert to MP3 using moviepy
            base, ext = os.path.splitext(audio_path)
            mp3_path = base + '.mp3'
            video_clip = VideoFileClip(audio_path)
            video_clip.audio.write_audiofile(mp3_path)
            video_clip.close()
            os.remove(audio_path)  # Clean up original file
            messagebox.showinfo("Success", "Download and conversion to MP3 completed!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download audio: {e}")


if __name__ == "__main__":
    root = Tk()
    app = YTDownloader(root)
    root.mainloop()
