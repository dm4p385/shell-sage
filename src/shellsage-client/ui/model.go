package ui

import (
	"fmt"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"strings"
	"time"

	"github.com/charmbracelet/bubbles/spinner"
	tea "github.com/charmbracelet/bubbletea"
	"shellsage-client/api-client"
)

const debounceDelay = 300 * time.Millisecond

type Model struct {
	Input       string
	Suggestions []string
	Cursor      int
	Err         error
	Loading     bool
	spinner     spinner.Model
}

type suggestionMsg []string
type errMsg error
type debounceMsg struct{}

func InitialModel() Model {
	s := spinner.New()
	s.Spinner = spinner.Dot

	return Model{
		Input:       "",
		Suggestions: []string{},
		Cursor:      0,
		Loading:     false,
		Err:         nil,
		spinner:     s,
	}
}

func (m Model) Init() tea.Cmd {
	return tea.Batch(m.spinner.Tick)
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
				m.Err = nil
				m.Input = m.Input[:len(m.Input)-1]
				return m, debounce()
			}
		default:
			if len(msg.Runes) > 0 {
				m.Err = nil
				m.Input += string(msg.Runes)
				return m, debounce()
			}
		}
	case spinner.TickMsg:
		var cmd tea.Cmd
		m.spinner, cmd = m.spinner.Update(msg)
		return m, cmd
	case suggestionMsg:
		m.Suggestions = msg
		m.Cursor = 0
		m.Loading = false
		m.Err = nil
	case debounceMsg:
		m.Loading = true
		return m, fetchSuggestions(m.Input)
	case errMsg:
		//fmt.Printf("errMsg type: %T\n", msg)
		if st, ok := status.FromError(msg); ok {
			switch st.Code() {
			case codes.DeadlineExceeded:
				m.Err = fmt.Errorf("🅧 Server timeout: suggestions took too long")
			case codes.Unavailable:
				m.Err = fmt.Errorf(" 🅧 Server unavailable")
			default:
				m.Err = fmt.Errorf("🅧 gRPC error: %v", st.Message())
			}
		} else {
			m.Err = msg
		}
		m.Loading = false
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

func debounce() tea.Cmd {
	return tea.Tick(debounceDelay, func(t time.Time) tea.Msg {
		return debounceMsg{}
	})
}

func (m Model) View() string {
	var b strings.Builder
	b.WriteString("> " + m.Input + "\n")
	if m.Loading {
		b.WriteString(m.spinner.View() + " loading suggestions...\n")
	}

	if m.Err != nil {
		b.WriteString(fmt.Sprintf("[!] Error: %s\n", m.Err.Error()))
		b.WriteString("Press ESC to exit or type to retry...\n")
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
