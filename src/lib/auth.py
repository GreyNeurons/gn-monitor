from keycloak import KeycloakAdmin, KeycloakOpenID, KeycloakError
from src.config import settings


keycloak_url = settings.KEYCLOAK_URL
realm_name = settings.REALM_NAME
client_id = settings.CLIENT_ID
client_secret_key = settings.CLIENT_SECRET
admin_username = settings.ADMIN_USERNAME
admin_password = settings.ADMIN_PASSWORD

print(f"keycloack_url :{keycloak_url}\n")
print(f"realm_name :{realm_name}\n")
print(f"client_id:{client_id}\n")
print(f"client_secret_key :{client_secret_key}\n")
print(f"admin_username :{admin_username}\n")
print(f"admin_password :{admin_password}\n")



# Initialize Keycloak Admin client (for administrative tasks)
try:
    keycloak_admin = KeycloakAdmin(
        server_url=keycloak_url,
        username=admin_username,
        password=admin_password,
        realm_name=realm_name,
        client_id=client_id,
        client_secret_key=client_secret_key,
        verify=True,
    )
except KeycloakError as e:
    # TODO: Convert to log
    print(f"Error initializing Keycloak Admin client: {e}")
    raise

# Initialize Keycloak OpenID client (for user login, logout, etc.)
try:
    keycloak_openid = KeycloakOpenID(
        server_url=keycloak_url,
        client_id=client_id,
        realm_name=realm_name,
        client_secret_key=client_secret_key,
        verify=True,
    )
except KeycloakError as e:
    print(f"Error initializing Keycloak OpenID client: {e}")
    raise


# Function to create a new user (sign-up)
def create_user(username, password, first_name, last_name, email):
    try:
        user_id = keycloak_admin.create_user(
            {
                "username": username,
                "email": email,
                "firstName": first_name,
                "lastName": last_name,
                "enabled": True,
                "credentials": [
                    {"value": password, "type": "password", "temporary": False}
                ],
            }
        )
        print(f"User {username} created with ID: {user_id}")
        return user_id
    except KeycloakError as e:
        print(f"Error creating user {username}: {e}")
        raise


# Function to authenticate a user (sign-in)
def sign_in(username, password):
    try:
        token = keycloak_openid.token(username, password)
        print(f"Access Token: {token['access_token']}")
        return token
    except KeycloakError as e:
        print(f"!!!!Error signing in user {username}: {e}")
        raise


# Function to get roles associated with a user
def get_user_roles(user_id):
    try:
        # Get realm-level roles
        realm_roles = keycloak_admin.get_realm_roles_of_user(user_id)

        # Get client-level roles for all clients
        clients = keycloak_admin.get_clients()
        client_roles = {}
        for client in clients:
            client_id = client["id"]
            client_name = client["clientId"]
            roles = keycloak_admin.get_client_roles_of_user(user_id, client_id)
            client_roles[client_name] = roles

        print(f"Realm Roles for user {user_id}: {realm_roles}")
        print(f"Client Roles for user {user_id}: {client_roles}")

        return {"realm_roles": realm_roles, "client_roles": client_roles}
    except KeycloakError as e:
        print(f"!!!Error retrieving roles for user {user_id}: {e}")
        raise


# Function to reset a user's password
def reset_password(user_id, new_password):
    try:
        keycloak_admin.set_user_password(user_id, new_password, temporary=False)
        print(f"Password for user {user_id} has been reset.")
    except KeycloakError as e:
        print(f"!!!!Error resetting password for user {user_id}: {e}")
        raise


# Function to log out a user
def log_out(refresh_token):
    try:
        keycloak_openid.logout(refresh_token)
        print("User logged out.")

    except KeycloakError as e:
        print(f"!!!Error logging out user: {e}")
        raise

# Function to delete a user
def delete_user(user_id):
    try:
        keycloak_admin.delete_user(user_id)
        print("User deleted successfully.")

    except KeycloakError as e:
        print(f"!!!Error deleting user: {e}")
        raise


# Example usage
if __name__ == "__main__":
    
    # Sign up a new user
    user_id = create_user(
        "new_user1", "password123", "John", "Doe", "john.doe1@example.com"
    )
    

    # Sign in the user
    token = sign_in("new_user1", "password123")

    # Get roles associated with the user
    user_id = keycloak_admin.get_user_id("new_user1")
    roles = get_user_roles(user_id)

    # Reset the user's password
    reset_password(user_id, "newpassword123")

    # Log out the user
    log_out(token['refresh_token'])

    # Delete the user created earlier
    user_id = keycloak_admin.get_user_id("new_user1")
    keycloak_admin.delete_user(user_id)
