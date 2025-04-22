package main

import (
	"example.com/packages/internal/server"
)

func main() {
	r := server.BioServer()
	r.Run(":5005")

	//server := server.NewServer()

	//err := server.ListenAndServe()
	//if err != nil {
	//	panic(fmt.Sprintf("cannot start server: %s", err))
	//}
}
