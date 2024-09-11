import json
from datetime import datetime


class ContentManager:
    invalid_sections = ["providerName", "language", "lastUpdated"]
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_data()

    def load_data(self):
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

    def save_data(self):
        # Update the lastUpdated field with the current date and time
        self.data["lastUpdated"] = datetime.utcnow().isoformat() + "Z"

        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)
        print("Data saved successfully!")

    def print_sections(self, section):
        if section in self.data:
            for index, video in enumerate(self.data[section], start=1):
                print(f"{index}. {video['title']} - {video['id']}")
            print("---- End of List ----")
        else:
            print(f"Section '{section}' not found.")

    def add_content(self, section, new_content):
        if section in self.data:
            self.data[section].append(new_content)
        else:
            self.data[section] = [new_content]
        self.save_data()

    def edit_content(self, section, video_id, field, new_value):
        if section in self.data:
            for video in self.data[section]:
                if video["id"] == video_id:
                    if field in video:
                        video[field] = new_value
                    elif field in video["content"]:
                        video["content"][field] = new_value
                    self.save_data()
                    print(f"Video {video_id} in section '{section}' updated successfully!")
                    return
            print(f"Video with id {video_id} not found in section '{section}'.")
        else:
            print(f"Section '{section}' not found.")

    def delete_content(self, section, video_id):
        if section in self.data:
            original_length = len(self.data[section])
            self.data[section] = [video for video in self.data[section] if video["id"] != video_id]
            if len(self.data[section]) < original_length:
                self.save_data()
                print(f"Video with id {video_id} deleted successfully from section '{section}'!")
            else:
                print(f"Video with id {video_id} not found in section '{section}'.")
        else:
            print(f"Section '{section}' not found.")

    def get_all_video_ids(self, section):
        """Returns a list of all video IDs in a section."""
        if section in self.data:
            return [video["id"] for video in self.data[section]]
        else:
            print(f"Section '{section}' not found.")
            return []

    def get_video_fields(self, section, video_id):
        """Returns the fields for a given video ID in a section."""
        if section in self.data:
            for video in self.data[section]:
                if video["id"] == video_id:
                    # Combine the top-level fields and the content-specific fields
                    fields = list(video.keys()) + list(video["content"].keys())
                    return fields
            print(f"Video with id {video_id} not found in section '{section}'.")
        else:
            print(f"Section '{section}' not found.")
        return None

    @property
    def all_sections(self):
        return [section for section in self.data.keys() if section not in self.invalid_sections]

    def print_all_sections(self):
        """Prints all available sections in the content feed."""
        if self.all_sections:
            print("Available sections:")
            for section in self.all_sections:
                print(f"- {section}")
        else:
            print("No sections found.")
