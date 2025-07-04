from app import create_app
from dotenv import load_dotenv
import os


load_dotenv()
env = os.getenv('FLASK_ENV', 'development')

config_map = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig'
}

app = create_app(config_map.get(env))

if __name__ == '__main__':
    app.run()