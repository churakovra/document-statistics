import string


def test_correct_words_reading():
    text = "Hello  world! This is? TeSt senTence"
    words = [word.strip(string.punctuation).lower() for word in text.split()]

    assert words == ["hello", "world", "this", "is", "test", "sentence"]

def test_empty_words_no_exception():
    text = "  "
    words = [word.strip(string.punctuation).lower() for word in text.split()]

    assert words == []