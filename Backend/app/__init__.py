from flask import Flask
from flask_cors import CORS
from .models import db
from .extensions import ma, limiter, cache
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.Service_Tickets import service_tickets_bp
from .blueprints.parts import parts_bp
from flask_swagger_ui import get_swaggerui_blueprint



SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our API url (can of course be a local resource)

#creating swagger blueprint
swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Bagel's Repair Shop API"})


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    CORS(app)
    
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    print("USING DATABASE:", app.config["SQLALCHEMY_DATABASE_URI"])

    
    #Register Blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
    app.register_blueprint(parts_bp, url_prefix='/parts')
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)
    
    @app.route("/fix_pending_to_open")
    def fix_pending_to_open():
        from app.models import Service_Tickets
        updated = Service_Tickets.query.filter_by(status="Pending").update({"status": "Open"})
        db.session.commit()
        return f"Updated {updated} tickets from Pending to Open."

    return app
