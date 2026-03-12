from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.base import engine, Base


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        
        # Insert initial data if needed
        await insert_initial_data(conn)


async def insert_initial_data(conn):
    """Insert initial data into database"""
    # Check if admin user exists
    result = await conn.execute(
        text("SELECT COUNT(*) FROM users WHERE role = 'admin'")
    )
    admin_count = result.scalar()
    
    if admin_count == 0:
        # Insert admin user
        await conn.execute(
            text("""
                INSERT INTO users (name, email, phone, password_hash, role) 
                VALUES ('Admin', 'admin@dental.com', '+79001234567', 
                       '$2b$12$KIXIYz0QZq0QZq0QZq0QZuV5Yz0QZq0QZq0QZq0QZq0QZq0QZq0QZ', 'admin')
            """)
        )
        
        # Insert sample services
        await conn.execute(
            text("""
                INSERT INTO services (title, description, price, duration, image_url) VALUES 
                ('Консультация', 'Первичный осмотр и консультация стоматолога', 500.00, 30, '/images/services/consultation.jpg'),
                ('Ультразвуковая чистка', 'Профессиональная чистка зубов ультразвуком', 2000.00, 45, '/images/services/cleaning.jpg'),
                ('Пломбирование', 'Лечение кариеса и установка пломбы', 1500.00, 60, '/images/services/filling.jpg'),
                ('Протезирование', 'Установка коронок и мостов', 15000.00, 90, '/images/services/prosthetics.jpg'),
                ('Отбеливание', 'Профессиональное отбеливание зубов', 8000.00, 60, '/images/services/whitening.jpg')
            """)
        )
        
        await conn.commit()