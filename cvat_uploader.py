import os
import requests
import json

# ---------------------------------------------------------------------
# LOAD TOKEN SAFELY FROM A SEPARATE FILE
# ---------------------------------------------------------------------
def load_token():
    if not os.path.exists("cvat_token.txt"):
        raise RuntimeError(
            "❌ Token file missing.\n"
            "Create a file named cvat_token.txt containing ONLY your token."
        )
    with open("cvat_token.txt", "r") as f:
        return f.read().strip()


API_TOKEN = load_token()

CVAT_URL = "http://localhost:8080/api"
HEADERS = {"Authorization": f"Token {API_TOKEN}"}

# OPTIONAL: set a project ID if you want tasks inside a CVAT project.
PROJECT_ID = None
# PROJECT_ID = 5   # example


# ---------------------------------------------------------------------
# CREATE TASK
# ---------------------------------------------------------------------
def create_task(task_name):
    payload = {"name": task_name}
    if PROJECT_ID:
        payload["project_id"] = PROJECT_ID

    r = requests.post(f"{CVAT_URL}/tasks", headers=HEADERS, json=payload)
    r.raise_for_status()

    task_id = r.json()["id"]
    print(f"   ✔ Task created: {task_id} ({task_name})")
    return task_id


# ---------------------------------------------------------------------
# UPLOAD VIDEO
# ---------------------------------------------------------------------
def upload_video(task_id, video_path):
    print(f"   ⏳ Uploading video…")
    with open(video_path, "rb") as f:
        r = requests.post(
            f"{CVAT_URL}/tasks/{task_id}/data",
            headers=HEADERS,
            files={"client_files": (os.path.basename(video_path), f)},
            data={"image_quality": 70}
        )
    r.raise_for_status()
    print("   ✔ Video uploaded")


# ---------------------------------------------------------------------
# UPLOAD ANNOTATIONS
# ---------------------------------------------------------------------
def upload_annotations(task_id, xml_path):
    print(f"   ⏳ Uploading annotations…")
    with open(xml_path, "rb") as f:
        r = requests.put(
            f"{CVAT_URL}/tasks/{task_id}/annotations",
            headers=HEADERS,
            files={"annotation_file": (os.path.basename(xml_path), f)},
            data={"format": "CVAT for video", "action": "upload"}
        )
    r.raise_for_status()
    print("   ✔ Annotations uploaded")


# ---------------------------------------------------------------------
# FIND AND PROCESS ALL VIDEO + XML PAIRS
# ---------------------------------------------------------------------
def process_all(base="."):
    print("🚀 Starting CVAT auto-task creation…\n")

    for root, dirs, files in os.walk(base):
        videos = [f for f in files if f.lower().endswith(
            (".mp4", ".mov", ".avi", ".mkv")
        )]

        for v in videos:
            basename = os.path.splitext(v)[0]
            xml_name = basename + ".xml"

            if xml_name not in files:
                print(f"⚠️ No XML for {v} — skipping")
                continue

            video_path = os.path.join(root, v)
            xml_path = os.path.join(root, xml_name)

            print(f"\n⚡ Processing:")
            print(f"   VIDEO → {video_path}")
            print(f"   XML   → {xml_path}")

            # 1. Create CVAT task
            task_id = create_task(basename)

            # 2. Upload video
            upload_video(task_id, video_path)

            # 3. Upload annotations
            upload_annotations(task_id, xml_path)

    print("\n🏁 All tasks created successfully!")


if __name__ == "__main__":
    process_all(".")

