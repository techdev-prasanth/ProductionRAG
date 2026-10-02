from sqlalchemy import event

from accounts.models import User , UserProfile
from sqlalchemy.orm import Session


@event.listens_for(Session,"before_flush")
def create_user_profile(session: Session,flush_context,instances):
    for obj in session.new:
        if isinstance(obj,User) and obj.profile is None:
            obj.profile = UserProfile()
            print("User profile has been ctreated for ")

