def prompt_user(prompt_text: str, checks=None, show_options=False):
    print(prompt_text)
    user_input = input("> ")

    if checks and user_input not in checks:
        if show_options:
            print(f'Invalid input. Please try again. {checks}')
        else:
            print('Invalid input. Please try again.')
        print("-" * 30)
        return prompt_user(prompt_text, checks)

    return user_input
