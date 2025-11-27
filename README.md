🚀 CVAT Auto Task Creator (Video + Annotation Batch Import)

This script provides a fully automated pipeline for importing large video datasets into CVAT (Computer Vision Annotation Tool).
It detects all video/annotation pairs inside a directory tree and automatically:

Creates a new CVAT task for each video

Uploads the corresponding video file

Uploads the matching annotation file (CVAT XML format)

Supports optional integration with CVAT Projects

Runs completely hands-free over hundreds of files

Designed for large-scale drone datasets, tracking datasets, Air-to-Air FPV datasets, surveillance feeds, and computer vision research pipelines.

✨ Features

🔍 Auto-detects all video + .xml annotation pairs

🎥 Supports .mp4, .mov, .avi, .mkv

📤 Creates CVAT tasks automatically via API

📁 Uploads video data to each task

📝 Uploads CVAT-compatible annotation XML

🔧 Optional project assignment (via PROJECT_ID)

🔑 Safe token handling (token stored in cvat_token.txt)

🔄 Overwrite-safe and repeatable

🌲 Recursively scans entire dataset folder

⚠️ Skips pairs with missing annotations

💯 Works with hundreds of videos in batch mode

📁 Folder Structure

The script expects files formatted like:

dataset/
    clip1.mp4
    clip1.xml
    clip2.mp4
    clip2.xml
    subfolder/
        flightA.mov
        flightA.xml
        IR_01.mp4
        IR_01.xml


Each basename.mp4 must have a matching basename.xml.

🔑 Token Security

Create a file named:

cvat_token.txt


Containing ONLY your CVAT personal token.
This keeps sensitive credentials out of the script and repository.

▶️ Usage

Run from the dataset root:

python3 cvat_auto_task.py


The script will:

Discover all video files

For each, locate the matching XML annotation

Create a CVAT task

Upload video data

Upload annotations

Move to the next pair

Perfect for 100–1000+ videos.

🧠 Perfect For

Drone tracking datasets

RGB + IR paired videos

FPV pursuit datasets

Anti-UAV datasets

Surveillance pipelines

YOLO training datasets

Bulk CVAT annotation pipelines

🛠 Requirements

CVAT running (local or server)

A valid CVAT Personal Access Token

Python 3

Requests library:

pip install requests
