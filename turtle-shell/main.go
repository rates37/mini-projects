package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)

	for {
		fmt.Print("🐢 < $ ")
		input, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading input:", err)
			continue
		}

		fmt.Fprintln(os.Stdout, "🐢 💬:", input)
	}
}
