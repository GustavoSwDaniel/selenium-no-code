from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from infrastructure.container import Container
from infrastructure.exception import BadRequest, ValidationException

from selenium.common.exceptions import NoSuchElementException

from infrastructure.middlewares.exception_handler import generic_request_exception_handler, selenium_not_found_element_exception_handler, validation_exception_handler

def create_app() -> FastAPI:
    app = FastAPI()
    container = Container()

    app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, 
                       allow_methods=['*'], allow_headers=['*'])


    from presentation.endpoints.tests import controller as test_controllers
    test_controllers.configure(app)

    container.wire([test_controllers])

    app.add_exception_handler(BadRequest, handler=generic_request_exception_handler)
    app.add_exception_handler(Exception, handler=generic_request_exception_handler)
    app.add_exception_handler(NoSuchElementException, handler=selenium_not_found_element_exception_handler)
    app.add_exception_handler(ValidationException, handler=validation_exception_handler)

    return app


api_app = create_app()

if __name__ == '__main__':
    uvicorn.run('app:api_app', host='0.0.0.0', port=8080, reload=True)