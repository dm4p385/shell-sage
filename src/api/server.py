import threading
from concurrent import futures
import grpc
import shellsage_pb2
import shellsage_pb2_grpc

from src.prediction_engine.engine import ShellSageCore
from src.utils.logger import setup_logger


logger = setup_logger()

# Streaming version of ShellSageServicer
class ShellSageServicer(shellsage_pb2_grpc.ShellSageServiceServicer):
    def __init__(self):
        self.engine = ShellSageCore()
        logger.info(f"ShellSageServicer initialized! {threading.get_ident()}")

    def get_suggestions(self, prompt):
        results = self.engine.process_query(prompt)
        if results:
            return results
        logger.info("No suggestions found")

    def Autocomplete(self, request_iterator, context):
        for request in request_iterator:
            logger.info(f"Received prompt: {request.prompt}")
            suggestions = self.get_suggestions(request.prompt)
            yield shellsage_pb2.SuggestionResponse(suggestions=suggestions)

# Standard gRPC server setup
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shellsage_pb2_grpc.add_ShellSageServiceServicer_to_server(ShellSageServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("Streaming ShellSage server running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
