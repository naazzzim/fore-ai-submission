from typing import List, Optional
from app.models.user import User, UserCreate, UserUpdate


class UserService:
    """Service for user operations"""

    def __init__(self):
        # Mock database
        self.users = {
            1: User(id=1, username="user1", email="user1@example.com", is_active=True),
            2: User(id=2, username="user2", email="user2@example.com", is_active=True),
        }

    def list_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        """List all users with pagination"""
        users = list(self.users.values())
        return users[skip : skip + limit]

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)

    def create_user(self, user: UserCreate) -> User:
        """Create a new user"""
        new_id = max(self.users.keys()) + 1 if self.users else 1
        new_user = User(id=new_id, **user.model_dump())
        self.users[new_id] = new_user
        return new_user

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update a user"""
        if user_id not in self.users:
            return None
        existing_user = self.users[user_id]
        update_data = user_update.model_dump(exclude_unset=True)
        updated_user = existing_user.model_copy(update={**update_data})
        self.users[user_id] = updated_user
        return updated_user

    def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
