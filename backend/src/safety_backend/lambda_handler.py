from mangum import Mangum

from safety_backend.app import create_app

app = create_app()
handler = Mangum(app)
