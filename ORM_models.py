from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine

from sqlalchemy.orm import aliased
import uuid


Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    id = Column('idx_player_id',String(36), primary_key = True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True)
    
    #Realtionship
    proAccounts = relationship('ProAccount', back_populates='player')

class ProAccount(Base):
    __tablename__ = 'proAccounts'

    id = Column('idx_pro_account_id',String(36), primary_key = True,default=lambda: str(uuid.uuid4()))
    accountName = Column('account_name',String(100))
    tagline = Column(String)
    server = Column(String)
    isTournamentRealm = Column(Boolean)
    #ForeignKey
    playerId = Column(String(36), ForeignKey(players.id))

    #relationship
    player = relationship('Player', back_populates='proAccounts')

class Tournament(Base):
    __tablename__ = 'tournaments'
    
    id = Column('idx_Tournament_id',Integer, primary_key= True, autoincrement= True)
    name = Column(String)
    shortName = Column('short_name', String)
    startTime = Column('start_time', Integer)
    endTime = Column('end_time', Integer)
    totalRounds = Column('total_rounds',Integer)

    #Relationship
    tournamentRounds = relationship('TournamentRound',back_populates='tournament')

class TournamentRound(Base):
    __tablename__ = 'tournamentRounds'
    id = Column('idx_tournament_rounds_id',Integer,primary_key=True,autoincrement=True)
    roundNumber = Column('round_number',Integer)
    estStartTime =Column('est_start_time',Integer)
    estEndTime = Column('est_end_time',Integer)
    cutAfter = Column('cut_after',Boolean)

    #ForeignKey
    tournamentId = Column('tournament_id',Integer,ForeignKey("tournaments.id"))

    #Relationship
    tournament = relationship('Tournament',back_populates='tournamentRounds')



def update_player_name(player_id, new_name):
    player = session.query(Player).filter(Player.id == player_id).first()
    if player: 
        player.name = new_name 
        session.commit()
        print(f"Updated Player {player_id} -> {new_name}")
    else:
        print("Player not found")

