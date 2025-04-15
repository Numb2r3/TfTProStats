from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine

from sqlalchemy.orm import aliased
import uuid


Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    player_id = Column(String(36), primary_key = True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable = False )
    
    #Realtionship
    pro_accounts = relationship('ProAccount', back_populates='player')

class ProAccount(Base):
    __tablename__ = 'pro_accounts'

    pro_account_id = Column(String(36), primary_key = True,default=lambda: str(uuid.uuid4()))
    account_name = Column(String(100))
    tagline = Column(String)
    server = Column(String)
    is_tournament_realm = Column(Boolean)
   
    #ForeignKey
    player_id = Column(String(36), ForeignKey("players.player_id"))
    
    #relationship
    player = relationship('Player', back_populates='pro_accounts')

class Tournament(Base):
    __tablename__ = 'tournaments'
    
    tournament_id = Column(Integer, primary_key= True, autoincrement= True)
    name = Column(String)
    short_name = Column(String)
    start_time = Column(Integer)
    end_time = Column(Integer)
    total_rounds = Column(Integer)

    #Relationship
    rounds = relationship('TournamentRound',back_populates='tournament')

class TournamentRound(Base):
    __tablename__ = 'tournament_rounds'
    round_id = Column(Integer,primary_key=True,autoincrement=True)
    round_number = Column(Integer)
    est_start_time =Column(Integer)
    est_end_time = Column(Integer)
    cut_after = Column(Boolean)

    #ForeignKey
    tournament_id = Column(Integer,ForeignKey("tournaments.tournament_id"))

    #Relationship
    tournament = relationship('Tournament',back_populates='rounds')
    games = relationship('Game', back_populates='tournament_round')

class Game(Base):
    __tablename__ = 'games'

    game_id = Column(Integer,primary_key = True)
    game_type = Column(String(30))

    #ForeignKey
    round_id = Column(Integer,ForeignKey("tournament_rounds.round_id"))

    #Relationship
    round = relationship('TournamentRound',back_populates = 'games')




def update_player_name(player_id, new_name):
    player = session.query(Player).filter(Player.id == player_id).first()
    if player: 
        player.name = new_name 
        session.commit()
        print(f"Updated Player {player_id} -> {new_name}")
    else:
        print("Player not found")

