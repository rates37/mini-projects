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
			// handle ctrl + D:
			if err.Error() == "EOF" {
				fmt.Println("\nGoodbye!")
				break
			}
			fmt.Println("Error reading input:", err)
			continue
		}

		fmt.Fprintln(os.Stdout, "🐢 💬:", input)
	}
}
