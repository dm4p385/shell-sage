package api_client

import (
	"context"
	"fmt"
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
		return nil, fmt.Errorf("failed to connect: %v", err)
	}
	defer conn.Close()

	client := NewShellSageServiceClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	stream, err := client.Autocomplete(ctx)
	if err != nil {
		return nil, fmt.Errorf("error creating stream: %v", err)
	}

	// Send the prompt
	if err := stream.Send(&PromptRequest{Prompt: prompt}); err != nil {
		return nil, fmt.Errorf("failed to send prompt: %v", err)
	}

	// You could keep sending more prompts here if needed
	// stream.Send(&pb.PromptRequest{Prompt: "docker build"}) ...

	// Indicate you're done sending (for now)
	if err := stream.CloseSend(); err != nil {
		return nil, fmt.Errorf("error closing send stream: %v", err)
	}

	// Read the response
	var suggestions []string
	for {
		resp, err := stream.Recv()
		if err == io.EOF {
			break // Server closed stream
		}
		if err != nil {
			return nil, fmt.Errorf("error receiving suggestions: %v", err)
		}
		suggestions = append(suggestions, resp.Suggestions...)
	}

	return suggestions, nil
}
