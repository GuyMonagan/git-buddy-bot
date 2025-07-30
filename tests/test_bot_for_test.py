from bot_for_test import generate_git_command

def test_generate_git_command_known_action():
    assert generate_git_command("create_repo") == "git init"
    assert generate_git_command("add_files") == "git add ."
    assert generate_git_command("commit") == 'git commit -m "your commit message here"'

def test_generate_git_command_unknown_action():
    assert generate_git_command("hack_the_planet") == "Unknown command"
