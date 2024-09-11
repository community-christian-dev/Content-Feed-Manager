import generator
from manager import ContentManager
from generator import GenerateJSON
import cli


def quit_program(manager):
    quit()


def print_sections(manager):
    manager.print_sections()


def edit_content(manager):
    valid_ids = manager.get_all_video_ids()
    video_id = cli.prompt_user("Video ID", valid_ids)

    valid_fields = manager.get_video_fields(video_id)
    field = cli.prompt_user("Field", valid_fields)

    new_value = cli.prompt_user("New value", [])

    manager.edit_content(video_id, field, new_value)


def add_content(manager):
    new_content = generator.GenerateJSON()
    manager.add_content(new_content)


def delete_content(manager):
    valid_ids = manager.get_all_video_ids()
    video_id = cli.prompt_user("Video ID", valid_ids)
    manager.delete_content(video_id)


def save_data(manager):
    manager.save_data()


input_functions = {
    "q": quit_program,
    "p": print_sections,
    "a": add_content,
    "e": edit_content,
    "d": delete_content,
    "s": save_data
}


def main(file_path):
    manager = ContentManager(file_path)

    while True:
        user_input = cli.prompt_user("Select action", input_functions.keys(), show_options=True)
        input_functions[user_input](manager)


if __name__ == '__main__':
    file_path = 'content-feed.json'
    main(file_path)
