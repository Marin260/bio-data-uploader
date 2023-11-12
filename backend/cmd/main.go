package main

import (
	"example.com/packages/internal/server"
)

func main() {
	r := server.BioServer()

	r.Run(":8080")
}