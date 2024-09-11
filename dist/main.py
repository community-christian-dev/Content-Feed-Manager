import generator
from manager import ContentManager
from generator import GenerateJSON
import cli


def quit_program(manager):
    quit()


def print_sections(manager, section=None):
    if section is None:
        section = cli.prompt_user(f"Section {manager.all_sections}", manager.all_sections)
    manager.print_sections(section)


def edit_content(manager):
    section = cli.prompt_user(f"Section {manager.all_sections}", manager.all_sections)

    print_sections(manager, section=section)
    valid_ids = manager.get_all_video_ids(section)
    video_id = cli.prompt_user("Video ID", valid_ids)

    valid_fields = manager.get_video_fields(section, video_id)
    field = cli.prompt_user("Field", valid_fields)

    new_value = cli.prompt_user("New value", [])

    manager.edit_content(section, video_id, field, new_value)


def add_content(manager):
    all_sections = manager.all_sections
    section = cli.prompt_user(f"Section {all_sections}", [])

    if section not in all_sections:
        confirmation = cli.prompt_user(f"The inputted section '{section}' is not found and will create a new section.\n"
                                       f"Do you want to continue? (y/n)", ['y', 'n'], show_options=True)

        if confirmation == "y":
            new_content = generator.GenerateJSON()
            manager.add_content(section, new_content)
    else:
        new_content = generator.GenerateJSON()
        manager.add_content(section, new_content)


def delete_content(manager):
    section = cli.prompt_user(f"Section {manager.all_sections}", manager.all_sections)

    print_sections(manager, section=section)
    valid_ids = manager.get_all_video_ids(section)
    video_id = cli.prompt_user("Video ID", valid_ids)
    manager.delete_content(section, video_id)


def save_data(manager):
    manager.save_data()


def help(manager):
    print("Please select from the following options:")
    print(list(input_functions.keys()))


def print_all_sections(manager):
    manager.print_all_sections()


input_functions = {
    "quit": quit_program,
    "print": print_sections,
    "print all": print_all_sections,
    "add": add_content,
    "edit": edit_content,
    "del": delete_content,
    "save": save_data,
    "help": help
}


def main(file_path):
    manager = ContentManager(file_path)

    checks = list(input_functions.keys())

    while True:
        user_input = cli.prompt_user(f"Select action {checks}", checks)
        input_functions[user_input](manager)
        print("\n")


if __name__ == '__main__':
    path = 'content-feed.json'
    main(path)
