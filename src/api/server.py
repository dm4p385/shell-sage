import signal
import threading
from concurrent import futures

import asyncio
import grpc

from src.protobuf import shellsage_pb2, shellsage_pb2_grpc
from src.prediction_engine.engine import ShellSageCore
from src.utils.logger import setup_logger


logger = setup_logger()

# Streaming version of ShellSageServicer
class ShellSageServicer(shellsage_pb2_grpc.ShellSageServiceServicer):
    def __init__(self):
        self.engine = ShellSageCore()
        logger.info(f"ShellSageServicer initialized! thread: {threading.get_ident()}")

    def get_suggestions(self, prompt):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        results = loop.run_until_complete(self.engine.process_query(prompt))
        if results:
            logger.info(f"Returned {len(results)} results!")
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

    # Setup graceful shutdown
    shutdown_event = threading.Event()

    def handle_sigterm(*_):
        logger.info("Shutdown signal received. Shutting down gracefully...")
        shutdown_event.set()
        server.stop(grace=5)  # Wait 5 seconds for ongoing RPCs

    # Catch Ctrl+C and SIGTERM
    signal.signal(signal.SIGINT, handle_sigterm)
    signal.signal(signal.SIGTERM, handle_sigterm)

    shutdown_event.wait()
    logger.info("Server has shut down.")
if __name__ == '__main__':
    serve()
