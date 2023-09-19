import encryption

def test_encryption():
    '''Test encryption algorithm'''
    original_string = 'This is the original string'
    encrypted_string = encryption.encrypt_message(original_string)
    assert original_string != encrypted_string

def test_decryption():
    '''Test decryption'''
    original_string = 'This is the original string'
    decrypted_string = encryption.decrypt_message(encryption.encrypt_message(original_string)).decode()
    assert original_string == decrypted_string