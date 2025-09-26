# app.py

from flask import Flask, request, jsonify

# Create a new Flask web server
app = Flask(__name__)

# This is our "database" for now - just a simple list in memory
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]
# A counter to make sure new users get a unique ID
next_user_id = 3

# --- API Routes ---

# GET /users  (Get all users)
@app.route('/users', methods=['GET'])
def get_all_users():
    """This function returns the full list of users."""
    return jsonify(users)

# POST /users  (Create a new user)
@app.route('/users', methods=['POST'])
def create_user():
    """This function creates a new user and adds them to the list."""
    global next_user_id
    # Get the name and email from the incoming request data
    data = request.json
    new_user = {
        'id': next_user_id,
        'name': data['name'],
        'email': data['email']
    }
    # Add the new user to our list
    users.append(new_user)
    # Increase the ID for the next user
    next_user_id += 1
    # Return the new user's info with a "Created" status code
    return jsonify(new_user), 201

# GET /users/1  (Get a single user by their ID)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    """This function finds and returns a single user by their ID."""
    # Loop through the list to find the user with the matching ID
    for user in users:
        if user['id'] == user_id:
            return jsonify(user)
    # If the loop finishes without finding the user, return an error
    return jsonify({"error": "User not found"}), 404

# PUT /users/1  (Update a user)
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """This function finds a user and updates their info."""
    data = request.json
    # Loop through the list to find the user
    for user in users:
        if user['id'] == user_id:
            # Update their name and email
            user['name'] = data['name']
            user['email'] = data['email']
            return jsonify(user)
    # If user isn't found, return an error
    return jsonify({"error": "User not found"}), 404

# DELETE /users/1  (Delete a user)
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """This function finds a user and removes them from the list."""
    # Use a list comprehension to create a new list without the deleted user
    user_to_delete = None
    for user in users:
        if user['id'] == user_id:
            user_to_delete = user
            break

    if user_to_delete:
        users.remove(user_to_delete)
        return jsonify({"message": "User deleted"}), 200
    # If user isn't found, return an error
    return jsonify({"error": "User not found"}), 404

# This part runs the app when you execute "python app.py"
if __name__ == '__main__':
    app.run(debug=True)