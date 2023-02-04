from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .model_base import Base, ImageDB, UserDB

# 允许多线程
db_name = "pixiv_image.db"
check_same_thread = False
engine = create_engine('sqlite:///' + db_name, connect_args={"check_same_thread": check_same_thread})

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
# 生成索引
session.execute('CREATE INDEX if not exists image_id_index ON images (id)')
