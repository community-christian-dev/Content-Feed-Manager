import json
from datetime import datetime


class ContentManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_data()
        self.print_sections()

    def load_data(self):
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

    def save_data(self):
        # Update the lastUpdated field with the current date and time
        self.data["lastUpdated"] = datetime.utcnow().isoformat() + "Z"

        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)
        print("Data saved successfully!")

    def print_sections(self):
        for index, video in enumerate(self.data["CKIDS"], start=1):
            print(f"{index}. {video['title']} - {video['id']}")
        print("---- End of List ----")

    def add_content(self, new_content):
        self.data["CKIDS"].append(new_content)
        self.save_data()

    def edit_content(self, video_id, field, new_value):
        for video in self.data["CKIDS"]:
            if video["id"] == video_id:
                if field in video:
                    video[field] = new_value
                elif field in video["content"]:
                    video["content"][field] = new_value
                self.save_data()
                print(f"Video {video_id} updated successfully!")
                return
        print(f"Video with id {video_id} not found.")

    def delete_content(self, video_id):
        original_length = len(self.data["CKIDS"])
        self.data["CKIDS"] = [video for video in self.data["CKIDS"] if video["id"] != video_id]
        if len(self.data["CKIDS"]) < original_length:
            self.save_data()
            print(f"Video with id {video_id} deleted successfully!")
        else:
            print(f"Video with id {video_id} not found.")

    def get_all_video_ids(self):
        """Returns a list of all video IDs."""
        return [video["id"] for video in self.data["CKIDS"]]

    def get_video_fields(self, video_id):
        """Returns the fields for a given video ID."""
        for video in self.data["CKIDS"]:
            if video["id"] == video_id:
                # Combine the top-level fields and the content-specific fields
                fields = list(video.keys()) + list(video["content"].keys())
                return fields
        print(f"Video with id {video_id} not found.")
        return None


# # Example usage
# file_path = "content-feed.json"
# manager = ContentManager(file_path)
#
# # Print existing videos
# manager.print_sections()
#
# # Edit content
# manager.edit_content("studentministry-September-15th-Rule-of-Life-2024-09-15", "title", "Updated Rule of Life")
#
# # Delete content
# manager.delete_content("00202409151725760788")
