# 📁 File Organizer

Organize all media files in a directory (and its sub‑directories) into sensible folders:
* **Video_Portrait** – portrait‑oriented videos
* **Video_Landscape** – landscape‑oriented videos
* **Pictures** – standard image files
* **GIF** – animated GIFs
* **Others** – any other file types

The script automatically creates the target folders, moves files accordingly, and cleans up empty directories.

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| **Video orientation detection** | Uses `moviepy` to determine if a video is portrait or landscape. |
| **Image detection** | Uses `Pillow` to distinguish GIFs from other images. |
| **Recursive processing** | Scans all sub‑folders, ignoring hidden files (e.g., `._*`). |
| **Error handling** | Logs permission errors, missing files, and any unexpected issues. |
| **Cleanup** | Removes empty directories after moving files. |
| **Logging** | Informative console output with timestamps. |

---

## 📦 Prerequisites

Python 3.8+ is required.  


Install the dependencies:
```bash
pip install -r requirements.txt
```

---

## 🔧 Usage

```bash
python main.py /path/to/your/media/folder
```

If you omit the folder argument, the script will prompt you to input one.

**Example**

```bash
$ python organize_files.py ~/Pictures
2025-12-28 12:00:00 - INFO - Created folder: ~/Pictures/Video_Portrait
2025-12-28 12:00:00 - INFO - Created folder: ~/Pictures/Video_Landscape
2025-12-28 12:00:00 - INFO - Created folder: ~/Pictures/Pictures
2025-12-28 12:00:00 - INFO - Created folder: ~/Pictures/GIF
2025-12-28 12:00:00 - INFO - Created folder: ~/Pictures/Others
2025-12-28 12:00:01 - INFO - Moving sample.mp4 to Video_Portrait
2025-12-28 12:00:01 - INFO - Moving photo.jpg to Pictures
...
2025-12-28 12:00:05 - INFO - Removed empty directory: ~/Pictures/old
```

---

## 🧩 How It Works

1. **Directory creation** – Ensures all target folders exist.
2. **File walk** – Recursively iterates through `src_folder`.
3. **Classification**
    * Video → portrait/landscape via `moviepy`.
    * Image → GIF or standard pictures via `Pillow`.
    * Anything else → `Others`.
4. **Move** – Uses `shutil.move()` to relocate each file.
5. **Cleanup** – Bottom‑up walk removes any now‑empty directories.

---

## 🤝 Contributing

Feel free to open issues or pull requests. If you add a new feature or improve performance, let me know!

---

## 📄 License

MIT © 2025 – Feel free to use, modify, and distribute.

---