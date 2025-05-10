import mongo

def create_user_in_db(username: str, password: str, email: str):
    
    querry = {
        "username": username,
        "password": password,
        "email": email
    }
    res = mongo.create_user(querry)
    
    if not isinstance(res, dict):
        return res
    
    error = res.get('keyValue')
    
    if "username" in error:
        return {"error": "El nombre de usuario ya existe"}
    if "email" in error:
        return {"error": "El email ya existe"}
    return {"error": "Error al crear el usuario"}
    

def get_user(username: str) -> dict:
   return mongo.get_user(username)

if __name__ == "__main__":
    mongo.init_connection()
    a = create_user_in_db("salo", "password", "salo@salo.com")
    print(a)
    
    