import controller as bot

def test_get_rest_correctly_converts_string():
    test_str = 'TESt wIth spACEs anD caPs'
    converted = bot.get_rest_from_user(test_str)
    goal_string = 'test-with-spaces-and-caps'
    assert converted == goal_string
