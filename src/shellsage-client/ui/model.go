package ui

import (
	"fmt"
	"strings"

	tea "github.com/charmbracelet/bubbletea"
	"shellsage-client/api-client"
)

type Model struct {
	Input       string
	Suggestions []string
	Cursor      int
	Err         error
}

type suggestionMsg []string
type errMsg error

func InitialModel() Model {
	return Model{}
}

func (m Model) Init() tea.Cmd {
	return nil
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.Type {
		case tea.KeyCtrlC, tea.KeyEsc:
			return m, tea.Quit
		case tea.KeyEnter:
			if m.Cursor < len(m.Suggestions) {
				fmt.Println(m.Suggestions[m.Cursor])
				return m, tea.Quit
			}
		case tea.KeyUp:
			if m.Cursor > 0 {
				m.Cursor--
			}
		case tea.KeyDown:
			if m.Cursor < len(m.Suggestions)-1 {
				m.Cursor++
			}
		case tea.KeyBackspace:
			if len(m.Input) > 0 {
				m.Input = m.Input[:len(m.Input)-1]
				return m, fetchSuggestions(m.Input)
			}
		default:
			if len(msg.Runes) > 0 {
				m.Input += string(msg.Runes)
				return m, fetchSuggestions(m.Input)
			}
		}
	case suggestionMsg:
		m.Suggestions = msg
		m.Cursor = 0
		m.Err = nil
	case errMsg:
		m.Err = msg
		m.Suggestions = []string{}
	}
	return m, nil
}

func fetchSuggestions(query string) tea.Cmd {
	return func() tea.Msg {
		s, err := api_client.StreamSuggestions(query)
		if err != nil {
			return errMsg(err)
		}
		return suggestionMsg(s)
	}
}

func (m Model) View() string {
	var b strings.Builder
	b.WriteString("> " + m.Input + "\n\n")
	if m.Err != nil {
		b.WriteString("Error: " + m.Err.Error())
		return b.String()
	}
	for i, s := range m.Suggestions {
		cursor := " "
		if i == m.Cursor {
			cursor = "➤"
		}
		b.WriteString(fmt.Sprintf("%s %s\n", cursor, s))
	}
	return b.String()
}
