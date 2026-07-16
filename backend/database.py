"""
Database connection and configuration for RiskShield-BFSI-X
Supports both SQLite (local development) and PostgreSQL (production)
"""

import os
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.pool import QueuePool, StaticPool
from contextlib import contextmanager

# ===== CONFIGURATION =====

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./riskshield.db"  # Default: SQLite for local development
)

print(f"📊 Database: {DATABASE_URL[:50]}..." if len(DATABASE_URL) > 50 else f"📊 Database: {DATABASE_URL}")

# Detect database type
IS_SQLITE = "sqlite" in DATABASE_URL.lower()
IS_POSTGRESQL = "postgresql" in DATABASE_URL.lower()

# ===== ENGINE SETUP =====

if IS_POSTGRESQL:
    # PostgreSQL / Supabase configuration with connection pooling
    POOL_SIZE = int(os.getenv("DATABASE_POOL_MAX", 10))
    MAX_OVERFLOW = 5
    POOL_TIMEOUT = int(os.getenv("DATABASE_POOL_TIMEOUT", 30))
    POOL_RECYCLE = 300
    
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=POOL_SIZE,
        max_overflow=MAX_OVERFLOW,
        pool_timeout=POOL_TIMEOUT,
        pool_pre_ping=True,
        pool_recycle=POOL_RECYCLE,
        connect_args={
            "connect_timeout": 10,
            "application_name": "riskshield-bfsi-x",
        },
        echo=False,
    )
    print("✅ PostgreSQL connection pooling enabled")
    
elif IS_SQLITE:
    # SQLite configuration for local development
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Use StaticPool for SQLite
        echo=False,
    )
    print("✅ SQLite database initialized (local)")
else:
    raise ValueError(f"Unsupported database URL: {DATABASE_URL}")

# ===== EVENT LISTENERS =====

@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Configure connection based on database type"""
    cursor = dbapi_conn.cursor()
    try:
        if IS_POSTGRESQL:
            cursor.execute("SET timezone = 'UTC'")
            cursor.execute("SET application_name = 'riskshield-bfsi-x'")
        elif IS_SQLITE:
            # SQLite performance pragmas
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("PRAGMA journal_mode = WAL")  # Write-Ahead Logging
    except Exception as e:
        print(f"⚠️  Warning setting connection options: {e}")
    finally:
        cursor.close()

# ===== BASE FOR MODELS =====

Base = declarative_base()

# ===== SESSION FACTORY =====

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ===== CONTEXT MANAGER =====

@contextmanager
def get_db_context():
    """
    Context manager for database sessions.
    Usage:
        with get_db_context() as db:
            db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"❌ Database error: {e}")
        raise
    finally:
        db.close()

# ===== FASTAPI DEPENDENCY =====

def get_db() -> Session:
    """
    FastAPI dependency for injecting database sessions into route handlers.
    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"❌ Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# ===== HEALTH CHECK =====

def test_db_connection() -> bool:
    """
    Test database connection without creating a full session.
    Useful for /health endpoints and startup checks.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

# ===== INITIALIZATION =====

def init_db():
    """
    Create all tables if they don't exist.
    Call this once at application startup.
    """
    print("📦 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables initialized")

def dispose_db():
    """
    Close all connections in the pool.
    Call this at application shutdown.
    """
    print("🔌 Disposing database connections...")
    engine.dispose()
    print("✅ Database connections closed")

# ===== DEBUG INFO =====

if __name__ == "__main__":
    print("\n📊 Database Configuration:")
    print(f"   Type: {'SQLite (Local)' if IS_SQLITE else 'PostgreSQL (Cloud)'}")
    print(f"   URL: {DATABASE_URL[:50]}..." if len(DATABASE_URL) > 50 else f"   URL: {DATABASE_URL}")
    if IS_POSTGRESQL:
        print(f"   Pool Size: {int(os.getenv('DATABASE_POOL_MAX', 10))}")
    print(f"\n🔍 Connection Test:")
    if test_db_connection():
        print("   ✅ Database connection successful!")
    else:
        print("   ❌ Database connection failed!")
