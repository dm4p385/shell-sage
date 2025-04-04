from concurrent import futures
import grpc
import shellsage_pb2
import shellsage_pb2_grpc

from src.prediction_engine.engine import ShellSageCore

# connect to core here
def get_suggestions(prompt):
    # return [
    #     f"{prompt} --help",
    #     f"{prompt} build",
    #     f"{prompt} run"
    # ]


# Streaming version of ShellSageServicer
class ShellSageServicer(shellsage_pb2_grpc.ShellSageServiceServicer):
    def Autocomplete(self, request_iterator, context):
        for request in request_iterator:
            print(f"Received prompt: {request.prompt}")
            suggestions = get_suggestions(request.prompt)
            yield shellsage_pb2.SuggestionResponse(suggestions=suggestions)

# Standard gRPC server setup
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shellsage_pb2_grpc.add_ShellSageServiceServicer_to_server(ShellSageServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("🚀 Streaming ShellSage server running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
