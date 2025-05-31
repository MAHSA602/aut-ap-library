import requests

# base url for library api
BASE_URL = 'http://127.0.0.1:8080/api/v1'

# test adding a book
def test_create_book():
    new_book = {'id': '4', 'title': 'Book D', 'author': 'Author D', 'isbn': '1234567893'}
    response = requests.post(f'{BASE_URL}/books', json=new_book)
    print("create book:", response.status_code, response.json())
    return response.json().get('id')

# test getting all books
def test_get_books():
    response = requests.get(f'{BASE_URL}/books')
    print("get all books:", response.status_code, response.json())

# test getting a book by id
def test_get_book(book_id):
    response = requests.get(f'{BASE_URL}/books/{book_id}')
    print(f"get book {book_id}:", response.status_code, response.json())

# test deleting a book
def test_delete_book(book_id):
    response = requests.delete(f'{BASE_URL}/books/{book_id}')
    print(f"delete book {book_id}:", response.status_code, response.json())

# test adding a user
def test_create_user():
    new_user = {
        'id': '3',
        'username': 'test_user',
        'name': 'Test User',
        'email': 'test@example.com'
    }
    response = requests.post(f'{BASE_URL}/users', json=new_user)
    print("create user:", response.status_code, response.json())
    return response.json().get('id')

# test getting all users
def test_get_users():
    response = requests.get(f'{BASE_URL}/users')
    print("get all users:", response.status_code, response.json())

# test getting a user by id
def test_get_user(user_id):
    response = requests.get(f'{BASE_URL}/users/{user_id}')
    print(f"get user {user_id}:", response.status_code, response.json())

# test updating a user
def test_update_user(user_id):
    updated_data = {
        'username': 'test_user_updated',
        'name': 'Updated User',
        'email': 'updated@example.com'
    }
    response = requests.put(f'{BASE_URL}/users/{user_id}', json=updated_data)
    print(f"update user {user_id}:", response.status_code, response.json())

# test reserving a book
def test_reserve_book(book_id, user_id):
    headers = {'user-id': user_id}  # Changed to lowercase 'user-id'
    response = requests.post(f'{BASE_URL}/books/{book_id}/reserve', headers=headers)
    print(f"reserve book {book_id} for user {user_id}:", response.status_code, response.json())

# test getting user reservations
def test_get_user_reservations(user_id):
    headers = {'user-id': user_id}  # Changed to lowercase 'user-id'
    response = requests.get(f'{BASE_URL}/users/{user_id}/reservations', headers=headers)
    print(f"get reservations for user {user_id}:", response.status_code, response.json())

# test canceling a reservation
def test_cancel_reservation(book_id, user_id):
    headers = {'user-id': user_id}  # Changed to lowercase 'user-id'
    response = requests.delete(f'{BASE_URL}/books/{book_id}/reserve', headers=headers)
    print(f"cancel reservation for book {book_id}:", response.status_code, response.json())

if __name__ == '__main__':
    print("library api test\n")
    # book tests
    book_id = test_create_book()
    test_get_books()
    test_get_book(book_id)
    # user tests
    user_id = test_create_user()
    test_get_users()
    test_get_user(user_id)
    test_update_user(user_id)
    # reservation tests
    test_reserve_book(book_id, user_id)
    test_get_user_reservations(user_id)
    test_cancel_reservation(book_id, user_id)
    test_get_user_reservations(user_id)
    # clean up
    test_delete_book(book_id)