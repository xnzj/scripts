def get_user_choice(options, prompt, default_value=None):
    try:
        print(prompt)

        for key, value in options.items():
            print(f"{key} -> {value}")

        while True:
            prompt2 = "Please enter the option"
            if default_value:
                prompt2 += f" (default: {default_value}): "
            else :
                prompt2 += ": "
            user_input = input(prompt2)
            user_input = user_input if user_input else default_value
            if user_input in options:
                return user_input
            else:
                print("Please enter a valid option.")
    except FileNotFoundError:
        print("")

def get_user_input(prompt, default_value=None):
    if default_value:
        user_input = input(f"{prompt} (default: '{default_value}'): ")
        return user_input if user_input else default_value
    else:
        return input(f"{prompt}: ")

def get_key_by_value(dictionary, search_value):
    for key, value in dictionary.items():
        if value == search_value:
            return key
    return None