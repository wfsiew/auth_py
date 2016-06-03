import cherrypy
from app import app

if __name__ == '__main__':
    cherrypy.tree.graft(app, '/app')
    
    cherrypy.server.unsubscribe()
    
    server = cherrypy._cpserver.Server()
    
    server.socket_host = "0.0.0.0"
    server.socket_port = 8080
    server.thread_pool = 30
    
    server.subscribe()
    
    cherrypy.engine.start()
    cherrypy.engine.block()
