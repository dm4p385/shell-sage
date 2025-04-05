package api_client

import (
	"context"
	"io"
	//"log"
	"time"

	"google.golang.org/grpc"
)

const (
	serverAddress = "localhost:50051"
)

// StreamSuggestions opens a bi-directional stream to send prompts and receive suggestions.
func StreamSuggestions(prompt string) ([]string, error) {
	conn, err := grpc.Dial(serverAddress, grpc.WithInsecure())
	if err != nil {
		return nil, err
	}
	defer conn.Close()

	client := NewShellSageServiceClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	stream, err := client.Autocomplete(ctx)
	if err != nil {
		return nil, err
	}

	if err := stream.Send(&PromptRequest{Prompt: prompt}); err != nil {
		return nil, err
	}

	if err := stream.CloseSend(); err != nil {
		return nil, err
	}

	var suggestions []string
	for {
		resp, err := stream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, err
		}
		suggestions = append(suggestions, resp.Suggestions...)
	}

	return suggestions, nil
}
