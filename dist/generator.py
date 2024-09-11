from datetime import datetime, timezone
import json
import cli
import os


class VideoObject:
    def __init__(self):
        self.url = None
        self.quality = None
        self.videoType = None


class ContentObject:
    def __init__(self):
        self.dateAdded = self.get_datetime()
        self.video = VideoObject()
        self.duration = None
        self.language = "en-US"

    def get_datetime(self):
        current_time = datetime.now(timezone.utc)
        return current_time.isoformat()


class GenreObject:
    area_map = {
        "ckids": "00",
        "studentministry": "01"
    }

    def __init__(self):
        self.id = None
        self.area = "ckids"
        self.title = None
        self.content = ContentObject()
        self.thumbnail = None
        self.shortDescription = None
        self.longDescription = None
        self.releaseDate = "09-08-24"
        self.rating = "G"

    def generate_id(self):
        new_id = self.area_map[self.area]
        new_id += self.releaseDate.replace("-", "")
        new_id += str(int(datetime.now(timezone.utc).timestamp()))
        return new_id


def load_used_ids(file_path="used_ids.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []


def save_used_ids(used_ids, file_path="used_ids.json"):
    with open(file_path, "w") as file:
        json.dump(used_ids, file)


def is_unique_id(new_id, used_ids):
    return new_id not in used_ids


def generate_unique_id(main_object, used_ids):
    while True:
        new_id = main_object.generate_id()
        if is_unique_id(new_id, used_ids):
            return new_id


def GenerateJSON():
    main_object = GenreObject()

    used_ids = load_used_ids()

    main_object.area = cli.prompt_user("Ministry area", ["ckids", "studentministry"])
    main_object.title = cli.prompt_user("Title")
    main_object.content.video.url = cli.prompt_user("URL")
    main_object.content.video.quality = cli.prompt_user("Quality", ["SD", "HD", "FHD"])
    main_object.content.video.videoType = cli.prompt_user("Video type", ["MP4"])
    main_object.content.duration = cli.prompt_user("Duration")
    main_object.thumbnail = cli.prompt_user("Thumbnail")
    main_object.shortDescription = cli.prompt_user("Short description")
    main_object.longDescription = cli.prompt_user("Long description")
    main_object.releaseDate = cli.prompt_user("Release date")

    # Generate a unique ID
    main_object.id = generate_unique_id(main_object, used_ids)

    # Save the new ID to the list of used IDs
    used_ids.append(main_object.id)
    save_used_ids(used_ids)

    json_object = parse_object(main_object)

    return json_object


def parse_object(obj: GenreObject):
    json_object = {
        "longDescription": obj.longDescription,
        "thumbnail": obj.thumbnail,
        "releaseDate": obj.releaseDate,
        "genres": [
            "educational"
        ],
        "id": obj.id,
        "shortDescription": obj.shortDescription,
        "title": obj.title,
        "content": {
            "duration": int(obj.content.duration),
            "videos": [
                {
                    "url": obj.content.video.url,
                    "quality": obj.content.video.quality,
                    "videoType": obj.content.video.videoType
                }
            ],
            "language": obj.content.language,
            "dateAdded": obj.content.dateAdded
        }
    }

    return json_object
