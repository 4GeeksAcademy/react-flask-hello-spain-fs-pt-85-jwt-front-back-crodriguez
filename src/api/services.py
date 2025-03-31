from api.models import User  # Asegúrate de que tu modelo User esté definido en models.py
from api.models import db

class UserService:
    @staticmethod
    def exist(email):
        """Verifica si un usuario con el email dado ya existe."""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(email, password):
        """Crea un nuevo usuario en la base de datos."""
        new_user = User(email=email, password=password)  # Asegúrate de que el modelo User tenga estos campos
        db.session.add(new_user)
        db.session.commit()
        return new_user