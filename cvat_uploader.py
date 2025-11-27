import os
import requests
import json

CVAT_HOST = "http://localhost:8080"

USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"


# ------------------------------------------------------------------------------
# LOGIN TO CVAT AND GET JWT TOKEN
# ------------------------------------------------------------------------------
def login():
    print("🔑 Logging into CVAT…")

    r = requests.post(
        f"{CVAT_HOST}/api/auth/login",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "username": USERNAME,
            "password": PASSWORD
        })
    )

    if r.status_code != 200:
        raise RuntimeError(f"❌ Login failed: {r.text}")

    token = r.json()["key"]
    print("   ✔ Login OK")
    return token


def get_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


# ------------------------------------------------------------------------------
# CREATE TASK
# ------------------------------------------------------------------------------
def create_task(name, headers):
    r = requests.post(
        f"{CVAT_HOST}/api/tasks",
        headers=headers,
        json={"name": name}
    )
    r.raise_for_status()
    task_id = r.json()["id"]
    print(f"   ✔ Task created: {task_id}")
    return task_id


# ------------------------------------------------------------------------------
# UPLOAD VIDEO
# ------------------------------------------------------------------------------
def upload_video(task_id, video_path, headers):
    print("   ⏳ Uploading video…")
    with open(video_path, "rb") as f:
        r = requests.post(
            f"{CVAT_HOST}/api/tasks/{task_id}/data",
            headers=headers,
            files={"client_files": (os.path.basename(video_path), f)},
            data={"image_quality": 70}
        )
    r.raise_for_status()
    print("   ✔ Video uploaded")


# ------------------------------------------------------------------------------
# UPLOAD ANNOTATION
# ------------------------------------------------------------------------------
def upload_xml(task_id, xml_path, headers):
    print("   ⏳ Uploading annotations…")
    with open(xml_path, "rb") as f:
        r = requests.put(
            f"{CVAT_HOST}/api/tasks/{task_id}/annotations",
            headers=headers,
            files={"annotation_file": (os.path.basename(xml_path), f)},
            data={
                "format": "CVAT for video 1.1",
                "action": "upload"
            }
        )
    r.raise_for_status()
    print("   ✔ Annotation uploaded")


# ------------------------------------------------------------------------------
# MAIN PIPELINE
# ------------------------------------------------------------------------------
def process_all():
    print("🚀 Starting CVAT 2.50 auto-task creation…\n")

    token = login()
    headers = get_headers(token)

    for root, dirs, files in os.walk("."):
        videos = [f for f in files if f.lower().endswith(
            (".mp4", ".mov", ".avi", ".mkv"))]

        for v in videos:
            basename = v.rsplit(".", 1)[0]
            xml_name = basename + ".xml"

            if xml_name not in files:
                print(f"⚠️ Missing XML for: {v}")
                continue

            video_path = os.path.join(root, v)
            xml_path = os.path.join(root, xml_name)

            print(f"\n⚡ Processing:")
            print(f"   VIDEO → {video_path}")
            print(f"   XML   → {xml_path}")

            task_id = create_task(basename, headers)
            upload_video(task_id, video_path, headers)
            upload_xml(task_id, xml_path, headers)

    print("\n🏁 All tasks uploaded successfully!")


if __name__ == "__main__":
    process_all()
