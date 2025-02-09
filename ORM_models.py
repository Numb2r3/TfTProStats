from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String, unique=True)

def update_player_name(player_id, new_name):
    player = session.query(Player).filter(Player.id == player_id).first()
    if player: 
        player.name = new_namesession.commit()
        print(f"Updated Player {player_id} -> {new_name}")
    else:
        print("Player not found")