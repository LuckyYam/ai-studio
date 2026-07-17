from auth.passwords import hash_password, validate_password


def test_hash_password_is_not_plaintext():
    hashed = hash_password('password123')
    assert hashed != 'password123'
    assert hashed.startswith('$2b$') or hashed.startswith('$2a$')


def test_hash_password_is_salted_and_nondeterministic():
    h1 = hash_password('password123')
    h2 = hash_password('password123')
    assert h1 != h2


def test_validate_password_accepts_correct_password():
    hashed = hash_password('my-password1')
    assert validate_password('my-password1', hashed) is True


def test_validate_password_rejects_wrong_password():
    hashed = hash_password('my-password')
    assert validate_password('my-password2', hashed) is False


def test_validate_password_is_case_sensitive():
    hashed = hash_password('my-password1')
    assert validate_password('My-Password1', hashed) is False


def test_validate_password_rejects_empty_password_against_real_hash():
    hashed = hash_password('my-password')
    assert validate_password('', hashed) is False
