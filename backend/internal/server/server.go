package server

import (
	"fmt"
	"os/exec"
)
func main(){
	fmt.Println("hello world")
	err := exec.Command("python3", "./py/test.py").Run()
	fmt.Println(err)
}