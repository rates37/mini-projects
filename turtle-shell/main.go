package main

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"strings"
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

		// split arguments:
		input = strings.TrimSpace(input)
		if input == "" { // ignore empty input
			continue
		}
		args := strings.Split(input, " ")

		// check for exit command:
		if args[0] == "exit" {
			if len(args) > 1 {
				// return exit code if provided:
				fmt.Printf("Exiting with code %s\n", args[1])
				// check args[1] is numeric:
				var exitCode int
				if _, err := fmt.Sscanf(args[1], "%d", &exitCode); err != nil {
					fmt.Println("Invalid exit code, exiting with code 1")
					os.Exit(1)
				} else {
					// convert to int and exit with code:
					fmt.Sscanf(args[1], "%d", &exitCode)
					os.Exit(exitCode)
				}
			}
			fmt.Println("Goodbye!")
			break
		}

		// prepare to run the command:
		cmd := exec.Command(args[0], args[1:]...)
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		cmd.Stdin = os.Stdin

		// run the command:
		fmt.Fprintln(os.Stdout, "🐢: running command: `", input, "`")
		if err := cmd.Run(); err != nil {
			fmt.Fprintln(os.Stderr, "🐢: error:", err)
		}
	}
}
