package main

import (
	"fmt"

	tea "github.com/charmbracelet/bubbletea"
	"shellsage-client/ui"
)

func main() {
	p := tea.NewProgram(ui.InitialModel())
	if err := p.Start(); err != nil {
		fmt.Println("Error:", err)
	}
}
